import boto3

from services.football_dashboard.table_football_players import FootballPlayersTable
from services.football_dashboard.table_football_players_deprecated import (
    FootballPlayersTableDeprecated
)

dynamodb_res = boto3.resource('dynamodb', verify=False)


def migrate_data():
    football_players_table_deprecated = FootballPlayersTableDeprecated(dynamodb_res)
    football_players_table = FootballPlayersTable(dynamodb_res)

    print("Scanning the deprecated table for all items...")
    try:
        items = football_players_table_deprecated.scan(as_dict=True)
    except Exception as e:
        print(f"Error scanning deprecated table: {e}")
        return

    if not items:
        print("No items found in the deprecated table.")
        return

    print(f"Found {len(items)} items in the deprecated table.")

    try:
        football_players_table.put_items(items)
    except Exception as e:
        print(f"Error writing items to new table: {e}")
        return

    print("Data migration completed successfully.")


if __name__ == "__main__":
    migrate_data()
