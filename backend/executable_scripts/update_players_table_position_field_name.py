import boto3
from boto3.dynamodb.conditions import Attr

from services.football_dashboard.table_football_players import (
    FootballPlayersTable
)

dynamodb_res = boto3.resource('dynamodb', verify=False)


def update_players_table_position_field_name():
    football_players_table = FootballPlayersTable(dynamodb_res)

    response = football_players_table.scan(as_dict=True)

    for item in response:
        if 'position' in item:
            football_players_table.update_item(
                key={'id': item['id']},
                expression="SET #fp = :fp",
                values={
                    ':fp': item['position']
                },
                names={
                    '#fp': 'fieldPosition'
                },
                condition=Attr('id').exists()
            )

            # Remove the old field
            football_players_table.update_item(
                key={'id': item['id']},
                expression="REMOVE #pos",
                values={},
                names={
                    '#pos': 'position'
                },
                condition=Attr('id').exists()
            )

    print("Migration completed successfully for table: football_players, field: position.")


if __name__ == "__main__":
    update_players_table_position_field_name()
