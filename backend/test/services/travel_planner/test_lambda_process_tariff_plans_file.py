import pytest
import boto3
from decimal import Decimal

from test.utils import get_test_file_path, bucket_file_exists

MCPR_BUCKET = "test"


def get_tariff_plans_records():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table("mcprengine_test_tariff-plans").scan()


def get_import_running_status():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table("mcprengine_test_config").get_item(Key={"configKey": "TARIFF_IMPORT_RUNNING"})["Item"]["value"]


@pytest.fixture(scope='function')
def config_tariff_plans_import_not_running(config_table):
    boto3.resource("dynamodb").Table("mcprengine_test_config").put_item(
        Item={
            "configKey": "TARIFF_IMPORT_RUNNING",
            "value": ""
        })


@pytest.fixture(scope='function')
def config_tariff_plans_import_already_running(config_table):
    boto3.resource("dynamodb").Table("mcprengine_test_config").put_item(
        Item={
            "configKey": "TARIFF_IMPORT_RUNNING",
            "value": "MOS_TARIFFS-DELTA_correct.csv"
        })


@pytest.fixture(scope='function')
def tariff_plans_full_file_correct(s3bucket, mcpr_bucket):
    s3bucket.upload_file(
        get_test_file_path("catalogue_files/MOS_TARIFFS-FULL_correct.csv"),
        MCPR_BUCKET, 'CMT/TariffPlan/MOS_TARIFFS-FULL_correct.csv')


@pytest.fixture(scope='function')
def tariff_plans_delta_file_correct(s3bucket, mcpr_bucket):
    s3bucket.upload_file(
        get_test_file_path("catalogue_files/MOS_TARIFFS-DELTA_correct.csv"),
        MCPR_BUCKET, 'CMT/TariffPlan/MOS_TARIFFS-DELTA_correct.csv')


@pytest.fixture(scope='function')
def tariff_plans_delta_delete_lines_file_errors(s3bucket, mcpr_bucket):
    s3bucket.upload_file(
        get_test_file_path("catalogue_files/MOS_TARIFFS-DELTA_delete_lines_error.csv"),
        MCPR_BUCKET, 'CMT/TariffPlan/MOS_TARIFFS-DELTA_delete_lines_error.csv')


@pytest.fixture(scope='function')
def tariff_plans_header_mismatch_file(s3bucket, mcpr_bucket):
    s3bucket.upload_file(
        get_test_file_path("catalogue_files/MOS_TARIFFS-DELTA_additional_column.csv"),
        MCPR_BUCKET, 'CMT/TariffPlan/MOS_TARIFFS-DELTA_additional_column.csv')


@pytest.fixture(scope='function')
def tariff_plans_incorect_column_order_file(s3bucket, mcpr_bucket):
    s3bucket.upload_file(
        get_test_file_path("catalogue_files/MOS_TARIFFS-DELTA_incorrect_column_order.csv"),
        MCPR_BUCKET, 'CMT/TariffPlan/MOS_TARIFFS-DELTA_incorrect_column_order.csv')


@pytest.fixture(scope='function')
def tariff_plans_no_header_file(s3bucket, mcpr_bucket):
    s3bucket.upload_file(
        get_test_file_path("catalogue_files/MOS_TARIFFS-DELTA_no_header.csv"),
        MCPR_BUCKET, 'CMT/TariffPlan/MOS_TARIFFS-DELTA_no_header.csv')


@pytest.fixture(scope='function')
def tariff_plans_line_level_errors_file(s3bucket, mcpr_bucket):
    s3bucket.upload_file(
        get_test_file_path("catalogue_files/MOS_TARIFFS-DELTA_line_level_errors.csv"),
        MCPR_BUCKET, 'CMT/TariffPlan/MOS_TARIFFS-DELTA_line_level_errors.csv')


@pytest.fixture
def mock_decrypt_file(mocker):
    # Mock the decrypt_file method to simulate that decryption just renames the file.
    def fake_decrypt(self, enc_file, dec_file):
        open(dec_file, 'wb').write(open(enc_file, 'rb').read())

    mocker.patch('services.catalogue.catalogue_file_reader.CatalogueFileReader.decrypt_file', new=fake_decrypt)


def test_correct_tariff_plans_full_import(mocker, mock_decrypt_file, tariff_plans_full_file_correct, tariff_plans_table,
                                          config_table, mcpr_bucket, config_tariff_plans_import_not_running):
    from services.catalogue.lambda_process_tariff_plans_file import process_tariff_plans_file_handler
    mocker.patch("mcpr_lib.gpg.GPG._import_key")

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": MCPR_BUCKET},
                "object": {"key": "CMT/TariffPlan/MOS_TARIFFS-FULL_correct.csv"}
            }
        }]
    }

    process_tariff_plans_file_handler(event, None)

    records = get_tariff_plans_records()
    assert records["ScannedCount"] == 22

    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Processed/MOS_TARIFFS-FULL_correct.csv')
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Decrypted/Processed/MOS_TARIFFS-FULL_correct.csv')
    assert not get_import_running_status()


def test_correct_tariff_plans_delta_import(mocker, mock_decrypt_file, tariff_plans_delta_file_correct, tariff_plans_table,
                                           config_table, mcpr_bucket, config_tariff_plans_import_not_running):
    from services.catalogue.lambda_process_tariff_plans_file import process_tariff_plans_file_handler
    mocker.patch("mcpr_lib.gpg.GPG._import_key")

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": MCPR_BUCKET},
                "object": {"key": "CMT/TariffPlan/MOS_TARIFFS-DELTA_correct.csv"}
            }
        }]
    }

    process_tariff_plans_file_handler(event, None)

    records = get_tariff_plans_records()
    assert records["ScannedCount"] == 20
    # Assert how many records have the deleted flag set to true, but with the rest of the data still present
    deleted_records = [r for r in records["Items"] if r["deleted"]]
    assert len(deleted_records) == 2
    expected_delete_record_1 = {
        'partNumber': '117808',
        'packageName': '24mth 100GB Data Plan',
        'contractLength': Decimal('24'),
        'contractLengthUOM': 'Months',
        'lineRentalAmount': Decimal('16.6667'),
        'vatCode': Decimal('0.2'),
        'priceRiseAmount_1': Decimal('1.6667'),
        'priceRiseAmount_2': Decimal('0.1667'),
        'OOCPriceRise': Decimal('10.0'),
        'deleted': True
    }
    expected_delete_record_2 = {
        'partNumber': '117124',
        'packageName': 'Business Pro II Fibre 1 24m',
        'contractLength': Decimal('24'),
        'contractLengthUOM': 'Months',
        'lineRentalAmount': Decimal('32.5'),
        'vatCode': Decimal('0.2'),
        'priceRiseAmount_1': Decimal('3.25'),
        'priceRiseAmount_2': Decimal('0.325'),
        'OOCPriceRise': Decimal('10.0'),
        'deleted': True
    }
    assert deleted_records[0] == expected_delete_record_1
    assert deleted_records[1] == expected_delete_record_2

    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Processed/MOS_TARIFFS-DELTA_correct.csv')
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Decrypted/Processed/MOS_TARIFFS-DELTA_correct.csv')
    assert not get_import_running_status()


def test_import_already_running_error(mocker, mock_decrypt_file, tariff_plans_delta_file_correct, tariff_plans_table,
                                      config_table, mcpr_bucket, config_tariff_plans_import_already_running):
    from services.catalogue.lambda_process_tariff_plans_file import process_tariff_plans_file_handler
    from mcpr_lib.logger import Logger
    mocker.patch("mcpr_lib.gpg.GPG._import_key")
    # Patch the Logger.error method
    mock_error = mocker.patch.object(Logger, 'error')

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": MCPR_BUCKET},
                "object": {"key": "CMT/TariffPlan/MOS_TARIFFS-DELTA_correct.csv"}
            }
        }]
    }

    process_tariff_plans_file_handler(event, None)

    mock_error.assert_called_once()
    assert "Error processing file MOS_TARIFFS-DELTA_correct.csv: Import function still running." in mock_error.call_args[0][0]

    assert not get_tariff_plans_records()["Items"]
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Failed/MOS_TARIFFS-DELTA_correct.csv')
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Decrypted/Failed/MOS_TARIFFS-DELTA_correct.csv')
    assert get_import_running_status() == "MOS_TARIFFS-DELTA_correct.csv"


def test_header_mismatch_error(mocker, mock_decrypt_file, tariff_plans_header_mismatch_file, tariff_plans_table,
                               config_table, mcpr_bucket, config_tariff_plans_import_not_running):
    from services.catalogue.lambda_process_tariff_plans_file import process_tariff_plans_file_handler
    from mcpr_lib.logger import Logger
    mocker.patch("mcpr_lib.gpg.GPG._import_key")
    # Patch the Logger.error method
    mock_error = mocker.patch.object(Logger, 'error')

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": MCPR_BUCKET},
                "object": {"key": "CMT/TariffPlan/MOS_TARIFFS-DELTA_additional_column.csv"}
            }
        }]
    }

    process_tariff_plans_file_handler(event, None)

    mock_error.assert_called_once()
    assert "Error processing data row: File MOS_TARIFFS-DELTA_additional_column.csv failed to be processed. Header fields are different than the expected fields. Expected: ['Action_Code', 'Part_Number', 'Package_Name', 'Contract_Length', 'Contract_Length_UOM', 'LineRental_Amount', 'Vat_Code', 'Price_Rise_Amount1', 'Price_Rise_Amount2', 'Price_Rise_Amount3', 'OOC_Price_Rise'], Got: ['Action_Code', 'Part_Number', 'Package_Name', 'Contract_Length', 'Contract_Length_UOM', 'LineRental_Amount', 'Vat_Code', 'Price_Rise_Amount1', 'Price_Rise_Amount2', 'Price_Rise_Amount3', 'OOC_Price_Rise', 'Additional_Column']" in mock_error.call_args[0][0]

    assert not get_tariff_plans_records()["Items"]
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Failed/MOS_TARIFFS-DELTA_additional_column.csv')
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Decrypted/Failed/MOS_TARIFFS-DELTA_additional_column.csv')
    assert not get_import_running_status()


def test_incorect_column_order_error(mocker, mock_decrypt_file, tariff_plans_incorect_column_order_file, tariff_plans_table,
                                     config_table, mcpr_bucket, config_tariff_plans_import_not_running):
    from services.catalogue.lambda_process_tariff_plans_file import process_tariff_plans_file_handler
    from mcpr_lib.logger import Logger
    mocker.patch("mcpr_lib.gpg.GPG._import_key")

    mock_error = mocker.patch.object(Logger, 'error')

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": MCPR_BUCKET},
                "object": {"key": "CMT/TariffPlan/MOS_TARIFFS-DELTA_incorrect_column_order.csv"}
            }
        }]
    }

    process_tariff_plans_file_handler(event, None)

    mock_error.assert_called_once()
    assert "Error processing data row: File MOS_TARIFFS-DELTA_incorrect_column_order.csv failed to be processed. Header fields are different than the expected fields. Expected: ['Action_Code', 'Part_Number', 'Package_Name', 'Contract_Length', 'Contract_Length_UOM', 'LineRental_Amount', 'Vat_Code', 'Price_Rise_Amount1', 'Price_Rise_Amount2', 'Price_Rise_Amount3', 'OOC_Price_Rise'], Got: ['Part_Number', 'Package_Name', 'Contract_Length', 'Contract_Length_UOM', 'LineRental_Amount', 'Vat_Code', 'Price_Rise_Amount1', 'Price_Rise_Amount2', 'Price_Rise_Amount3', 'OOC_Price_Rise', 'Action_Code']" in mock_error.call_args[0][0]

    assert not get_tariff_plans_records()["Items"]
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Failed/MOS_TARIFFS-DELTA_incorrect_column_order.csv')
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Decrypted/Failed/MOS_TARIFFS-DELTA_incorrect_column_order.csv')
    assert not get_import_running_status()


def test_no_header_error(mocker, mock_decrypt_file, tariff_plans_no_header_file, tariff_plans_table,
                         config_table, mcpr_bucket, config_tariff_plans_import_not_running):
    from services.catalogue.lambda_process_tariff_plans_file import process_tariff_plans_file_handler
    from mcpr_lib.logger import Logger
    mocker.patch("mcpr_lib.gpg.GPG._import_key")

    mock_error = mocker.patch.object(Logger, 'error')

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": MCPR_BUCKET},
                "object": {"key": "CMT/TariffPlan/MOS_TARIFFS-DELTA_no_header.csv"}
            }
        }]
    }

    process_tariff_plans_file_handler(event, None)

    mock_error.assert_called_once()
    assert "Error processing data row: File MOS_TARIFFS-DELTA_no_header.csv failed to be processed. Header fields are different than the expected fields. Expected: ['Action_Code', 'Part_Number', 'Package_Name', 'Contract_Length', 'Contract_Length_UOM', 'LineRental_Amount', 'Vat_Code', 'Price_Rise_Amount1', 'Price_Rise_Amount2', 'Price_Rise_Amount3', 'OOC_Price_Rise'], Got: ['I', '109525', 'MIGRATION ONLY Vodafone Broadband and Home Phone Existing mobile customer FTR1', '18', 'Months', '7.5', '0.2', '0.75', '0.075', '', '10']" in mock_error.call_args[0][0]

    assert not get_tariff_plans_records()["Items"]
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Failed/MOS_TARIFFS-DELTA_no_header.csv')
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Decrypted/Failed/MOS_TARIFFS-DELTA_no_header.csv')
    assert not get_import_running_status()


def test_line_level_errors_error(mocker, mock_decrypt_file, tariff_plans_line_level_errors_file, tariff_plans_table,
                                 config_table, mcpr_bucket, config_tariff_plans_import_not_running):
    from services.catalogue.lambda_process_tariff_plans_file import process_tariff_plans_file_handler
    from mcpr_lib.logger import Logger
    mocker.patch("mcpr_lib.gpg.GPG._import_key")

    mock_error = mocker.patch.object(Logger, 'error')

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": MCPR_BUCKET},
                "object": {"key": "CMT/TariffPlan/MOS_TARIFFS-DELTA_line_level_errors.csv"}
            }
        }]
    }
    # 25 total rows, 13 with errors, 12 correct
    process_tariff_plans_file_handler(event, None)

    mock_error.assert_called_once()
    assert 'Tariff plans file processing failed for 13 rows with errors: [{\'line\': 2, \'column\': 0, \'action\': \'I\', \'error\': "Failed to convert row data: Error converting field contractLength to <class \'int\'>: invalid literal for int() with base 10: \'18A5\'"}, {\'line\': 4, \'column\': 0, \'action\': \'\', \'error\': \'Invalid action code \'}, {\'line\': 6, \'column\': 0, \'action\': \'A\', \'error\': "Failed to convert row data: Error converting field priceRiseAmount_1 to <class \'float\'>: could not convert string to float: \'PRICE_RISE_AMOUNT1\'"}, {\'line\': 9, \'column\': 1, \'action\': \'I\', \'error\': \'Part Number 120434# must be a numeric\'}, {\'line\': 11, \'column\': 1, \'action\': \'I\', \'error\': \'Part Number  must be a numeric\'}, {\'line\': 13, \'column\': 0, \'action\': \'I\', \'error\': "Failed to convert row data: Error converting field vatCode to <class \'float\'>: could not convert string to float: \'VAT_CODE\'"}, {\'line\': 15, \'column\': 0, \'action\': \'I\', \'error\': \'Row data: invalid value for contractLength: field required\'}, {\'line\': 16, \'column\': 0, \'action\': \'K\', \'error\': \'Invalid action code K\'}, {\'line\': 18, \'column\': 3, \'action\': \'I\', \'error\': \'Duration UOM must be one of: Days, Months, Years\'}, {\'line\': 20, \'column\': 0, \'action\': \'I\', \'error\': \'Row data: invalid value for vatCode: field required\'}, {\'line\': 21, \'column\': 3, \'action\': \'I\', \'error\': \'Duration UOM must be one of: Days, Months, Years\'}, {\'line\': 23, \'column\': 0, \'action\': \'I\', \'error\': "Failed to convert row data: Error converting field contractLength to <class \'int\'>: invalid literal for int() with base 10: \'A\'"}, {\'line\': 25, \'column\': 0, \'action\': \'I\', \'error\': \'Row data: invalid value for lineRentalAmount: field required\'}]' in mock_error.call_args[0][0]

    records = get_tariff_plans_records()
    assert records["ScannedCount"] == 12

    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Failed/MOS_TARIFFS-DELTA_line_level_errors.csv')
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Decrypted/Failed/MOS_TARIFFS-DELTA_line_level_errors.csv')
    assert not get_import_running_status()


def test_delete_lines_on_non_existent_part_numbers(mocker, mock_decrypt_file, tariff_plans_delta_delete_lines_file_errors, tariff_plans_table,
                                                   config_table, mcpr_bucket, config_tariff_plans_import_not_running):
    from services.catalogue.lambda_process_tariff_plans_file import process_tariff_plans_file_handler
    from mcpr_lib.logger import Logger
    mocker.patch("mcpr_lib.gpg.GPG._import_key")

    mock_error = mocker.patch.object(Logger, 'error')

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": MCPR_BUCKET},
                "object": {"key": "CMT/TariffPlan/MOS_TARIFFS-DELTA_delete_lines_error.csv"}
            }
        }]
    }
    # 25 total rows, 13 with errors, 12 correct
    process_tariff_plans_file_handler(event, None)

    mock_error.assert_called_once()
    assert "Tariff plans file processing failed for 2 rows with errors: [{'line': 1, 'column': 0, 'action': 'D', 'error': 'Failed to mark row as deleted: Tariff Plan 117127 not found: An error occurred (ConditionalCheckFailedException) when calling the UpdateItem operation: The conditional request failed'}, {'line': 2, 'column': 0, 'action': 'D', 'error': 'Failed to mark row as deleted: Tariff Plan 117809 not found: An error occurred (ConditionalCheckFailedException) when calling the UpdateItem operation: The conditional request failed'}]" in mock_error.call_args[0][0]

    records = get_tariff_plans_records()
    assert records["ScannedCount"] == 2

    deleted_records = [r for r in records["Items"] if r["deleted"]]
    assert len(deleted_records) == 2
    expected_delete_record_1 = {
        'partNumber': '109525',
        'packageName': 'INSERT LINE DELETED RIGHT AFTER',
        'contractLength': Decimal('18'),
        'contractLengthUOM': 'Months',
        'lineRentalAmount': Decimal('7.5'),
        'vatCode': Decimal('0.2'),
        'priceRiseAmount_1': Decimal('0.75'),
        'priceRiseAmount_2': Decimal('0.075'),
        'OOCPriceRise': Decimal('10.0'),
        'deleted': True
    }
    expected_delete_record_2 = {
        'partNumber': '117124',
        'packageName': 'AMMEND LINE DELETED RIGHT AFTER',
        'contractLength': Decimal('24'),
        'contractLengthUOM': 'Months',
        'lineRentalAmount': Decimal('32.5'),
        'vatCode': Decimal('0.2'),
        'priceRiseAmount_1': Decimal('3.25'),
        'priceRiseAmount_2': Decimal('0.325'),
        'OOCPriceRise': Decimal('10.0'),
        'deleted': True
    }
    assert deleted_records[0] == expected_delete_record_1
    assert deleted_records[1] == expected_delete_record_2

    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Failed/MOS_TARIFFS-DELTA_delete_lines_error.csv')
    assert bucket_file_exists(MCPR_BUCKET, 'CMT/TariffPlan/Decrypted/Failed/MOS_TARIFFS-DELTA_delete_lines_error.csv')
    assert not get_import_running_status()
