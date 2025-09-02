from mcpr_lib.logger import Logger
from mcpr_lib.lambda_middleware import lambda_logger
from services.catalogue.catalogue_file_reader import (
    TariffPlansFileReader,
    CatalogueProcessingException
)


@lambda_logger(log_input=True)
def process_tariff_plans_file_handler(event, _):
    s3_file_key = event["Records"][0]["s3"]["object"]["key"]

    try:
        tariff_plans_reader = TariffPlansFileReader(s3_file_key)
        tariff_plans_reader.process()
    except CatalogueProcessingException:
        nr_of_failures = len(tariff_plans_reader.errors)
        Logger().error(f"Tariff plans file processing failed for {nr_of_failures} rows "
                       f"with errors: {tariff_plans_reader.errors}")
