import boto3
from boto3.dynamodb.conditions import Attr

from services.football_dashboard.table_stadiums import StadiumsTable

dynamodb_res = boto3.resource('dynamodb', verify=False)


def update_stadiums_table_capacity_field_name():
    stadiums_table = StadiumsTable(dynamodb_res)

    response = stadiums_table.scan(as_dict=True)

    for item in response:
        if 'capacity' in item:
            stadiums_table.update_item(
                key={'id': item['id']},
                expression="SET #sc = :sc",
                values={
                    ':sc': item['capacity']
                },
                names={
                    '#sc': 'stadiumCapacity'
                },
                condition=Attr('id').exists()
            )

            # Remove the old field
            stadiums_table.update_item(
                key={'id': item['id']},
                expression="REMOVE #cap",
                values={},
                names={
                    '#cap': 'capacity'
                },
                condition=Attr('id').exists()
            )

    print("Migration completed successfully for table: stadiums, field: capacity.")


if __name__ == "__main__":
    update_stadiums_table_capacity_field_name()
