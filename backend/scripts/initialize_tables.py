#!/usr/bin/env python
import boto3

from argparse import ArgumentParser

db_res = boto3.resource("dynamodb")
db_client = boto3.client("dynamodb")

config_values = [
    {"configKey": "TARIFF_IMPORT_RUNNING", "value": ""},
    {"configKey": "DISCOUNT_IMPORT_RUNNING", "value": ""}
]

TABLES = {
    "config": config_values,
}


def populate_table(table_name: str, items: list):
    try:
        with db_res.Table(table_name).batch_writer() as writer:
            print("Table: " + table_name)
            for item in items:
                writer.put_item(Item=item)
    except db_client.exceptions.ResourceNotFoundException:
        print(f"Table {table_name} does not exist in the current environment")


if __name__ == "__main__":
    parser = ArgumentParser(description="Populate various tables with initial data")

    parser.add_argument("prefix", help="Tables prefix")
    args = parser.parse_args()

    if TABLES != {}:
        for table_name, table_items in TABLES.items():
            table_full_name = args.prefix + table_name
            try:
                populate_table(table_full_name, table_items)
            except Exception as ex:
                print(f"Error populating table {table_full_name}: {ex}")
                raise ex
    else:
        print("No tables to populate")
