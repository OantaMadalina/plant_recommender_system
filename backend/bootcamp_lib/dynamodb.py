# This file should be kept compatible with Python 3.7 syntax

from dataclasses import dataclass
import dataclasses
import time
from typing import Generic, TypeVar, List, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import os

import boto3  # type: ignore
from boto3.dynamodb.conditions import ConditionBase
from botocore.errorfactory import ClientError
from dynamodb_json import json_util

from bootcamp_lib.logger import Logger
from bootcamp_lib.dynamodb_model import DynamoDbModel


DYNAMO_RETURN_VALUES = Literal["NONE", "ALL_OLD", "UPDATED_OLD", "ALL_NEW", "UPDATED_NEW"]

T = TypeVar("T")


class QueryResult(Generic[T]):
    def __init__(self, count: int, scanned_count: int, items: List[T]):
        self.count = count
        self.scannedCount = scanned_count
        self.items = items


class UpdateStatements:
    def __init__(self, update_stmts=[], update_values={}, names={}):
        self.update_stmts = update_stmts
        self.update_values = update_values
        self.names = names


@dataclass
class RetryConfig:
    retriesCount: int = 1
    retryOnExceptions: List[str] = dataclasses.field(default_factory=list)
    retryDelay: float = 0.25


class DynamodbTable(Generic[T]):
    """Base class for representing a DynamoDB table with its operations.
    """
    table = ""
    model_type = DynamoDbModel

    def __init__(self, dynamodb_resource=None, model_type=None):
        if dynamodb_resource:
            self._dynamo_resource = dynamodb_resource
        else:
            self._dynamo_resource = boto3.resource("dynamodb")
        self._table_name = os.environ["environment"] + self.table
        self._table = self._dynamo_resource.Table(self._table_name)
        self._model_type = model_type or self.model_type

    def _prepare_fetch_fields(self):
        reserved_words = {
            "timestamp", "location", "value", "length", "breadth", "url", "status", "action",
            "uuid", "segment", "type", "error", "ttl", "dateTime"
        }
        params = {}
        params["ExpressionAttributeNames"] = {}

        model_fields = [field.name for field in dataclasses.fields(self._model_type)]
        for index, field in enumerate(model_fields):
            if field in reserved_words:
                params["ExpressionAttributeNames"]["#" + field] = field
                model_fields[index] = "#" + field

        if not params["ExpressionAttributeNames"]:
            del params["ExpressionAttributeNames"]

        params["ProjectionExpression"] = ",".join(model_fields)
        return params

    def get_item(
            self, key: dict, as_dict: bool = False, projection: str = "", names: dict = {},
            consistent_read: bool = False, model_type=None) -> T:
        """Gets an item from the database table.

        Args:
            key: the record key for which the record will be returned.
            as_dict: if True, returns the record as a dictionary, not as an object of type T
            projection: returned fields for the fetched item [ProjectionExpression]

        Returns:
            The fetched record, as an instance of model T if as_dict is False, else as a dictionary.
        """
        params = {
            "Key": key,
            "ConsistentRead": consistent_read
        }
        if projection:
            params["ProjectionExpression"] = projection
            if names:
                params["ExpressionAttributeNames"] = names
        elif not as_dict:
            params.update(self._prepare_fetch_fields())

        db_data = self._table.get_item(**params)

        if as_dict:
            return db_data
        elif "Item" in db_data:
            if not model_type:
                model_type = self._model_type
            return model_type(**db_data["Item"])
        return None

    def get_item_with_retry(
            self, key: dict, as_dict: bool = False, projection: str = "",
            consistent_read: bool = False, model_type=None, retries: int = 1) -> T:
        """Gets an item from the database table. Retry for a number of times if the result is null.

        Args:
            key: the record key for which the record will be returned.
            as_dict: if True, returns the record as a dictionary, not as an object of type T
            projection: returned fields for the fetched item [ProjectionExpression]

        Returns:
            The fetched record, as an instance of model T if as_dict is False, else as a dictionary.
        """

        for retry in range(0, retries + 1):
            consist_read = consistent_read or retry > 0
            item = self.get_item(
                key, as_dict=as_dict, projection=projection, consistent_read=consist_read,
                model_type=model_type
            )
            if item:
                return item
            if retry < retries:
                time.sleep(retry + 1)
        return None

    def get_items(
            self, keys: List[dict], as_dict: bool = False, projection: str = "", limit=0,
            names: dict = {}, model_type=None
    ) -> List[T]:
        params = {
            "RequestItems": {self._table.table_name: {}}
        }

        if projection:
            params["RequestItems"][self._table.table_name]["ProjectionExpression"] = projection
            if names:
                params["RequestItems"][self._table.table_name]["ExpressionAttributeNames"] = names
        elif not as_dict:
            params["RequestItems"][self._table.table_name].update(self._prepare_fetch_fields())

        all_items = []
        if limit > 0:
            keys = keys[:limit]

        if not model_type:
            model_type = self._model_type

        while keys:
            params["RequestItems"][self._table.table_name]["Keys"] = keys[:100]
            keys = keys[100:]

            get_response = self._dynamo_resource.meta.client.batch_get_item(**params)
            items = get_response["Responses"].get(self._table.table_name, [])
            if as_dict:
                all_items.extend(items)
            else:
                all_items.extend([model_type(**item) for item in items])

        return all_items

    def _retry_command(self, command, retry_config: RetryConfig):
        max_retries = 0 if not retry_config else retry_config.retriesCount
        exec_count = 0
        while exec_count <= max_retries:
            try:
                return command()
            except ClientError as err:
                if (not retry_config
                    or exec_count == max_retries
                    or (retry_config.retriesCount
                        and retry_config.retryOnExceptions
                        and err.response["Error"]["Code"] not in retry_config.retryOnExceptions)):
                    raise
                exec_count += 1
                Logger().info(
                    "Error %s on table %s, retry no. %d", err.response["Error"]["Code"],
                    self._table_name, exec_count)
                if retry_config.retryDelay > 0:
                    time.sleep(retry_config.retryDelay)

    def update_item(
        self, key: dict, expression: str, values: dict, names: dict = {},
        condition: ConditionBase = None, return_values: str = "NONE",
        retry_config: RetryConfig = None
    ):
        """Updates an item in the database table.

        Args:
            key: the record key for which the record will be returned.
            expression: update expression
            values: values used for updating the fields (e.g. {":field1": val1}, ...)
            names: redefined names used in the expression (e.g. {"#timestamp": timestamp, ...})
        """
        params = {
            "Key": key,
            "UpdateExpression": expression,
            "ReturnValues": return_values
        }

        if values:
            params["ExpressionAttributeValues"] = values

        if names:
            params["ExpressionAttributeNames"] = names

        if condition:
            params["ConditionExpression"] = condition

        if not retry_config:
            return self._table.update_item(**params)

        return self._retry_command(lambda: self._table.update_item(**params), retry_config)

    def put_item(
            self, item: Union[DynamoDbModel, dict], condition: ConditionBase = None,
            values: dict = {}, names: dict = {}, return_values: DYNAMO_RETURN_VALUES = "NONE"):
        """Inserts or overwrites an item in the database table.

        Args:
            item: object to insert/overwrite. It can be a DynamoDbModel instance or a dictionary

        Returns:
            The put_item operation result as it is returned by boto3 Table.put_item
        """
        if isinstance(item, DynamoDbModel):
            insert_item = item.to_dynamodb_dict()
        else:
            insert_item = item

        params = {
            "Item": insert_item,
            "ReturnValues": return_values
        }
        if condition:
            params["ConditionExpression"] = condition

        if values:
            params["ExpressionAttributeValues"] = values

        if names:
            params["ExpressionAttributeNames"] = names

        return self._table.put_item(**params)

    def put_items(self, items: List[DynamoDbModel]):
        """Batch inserts/overwrites items into the database table.

        Args:
            items: List of items to be inserted. Each item can be a DynamoDbModel object or a dict.
        """
        with self._table.batch_writer() as batch:
            for item in items:
                if isinstance(item, DynamoDbModel):
                    insert_item = item.to_dynamodb_dict()
                else:
                    insert_item = item
                batch.put_item(Item=insert_item)

    def delete_item(self, key: dict, return_values: DYNAMO_RETURN_VALUES = "NONE",
                    condition_expression=None, expression_attribute_values=None):
        """Deletes an item in the DynamoDB table.

        Args:
            key: the record key for the record to be deleted
            return_values: what the operation returns - one of the values:
                "NONE" (default), "ALL_OLD", "UPDATED_OLD", "ALL_NEW", "UPDATED_NEW"
            condition_expression: condition for deletion
            expression_attribute_values: values for the condition expression

        Returns:
            The delete_item operation result as it is returned by boto3 Table.delete_item
        """

        delete_args = {
            "Key": key,
            "ReturnValues": return_values
        }

        if condition_expression is not None:
            delete_args["ConditionExpression"] = condition_expression

        if expression_attribute_values is not None:
            delete_args["ExpressionAttributeValues"] = expression_attribute_values

        return self._table.delete_item(**delete_args)

    def delete_items(self, keys: List[dict]):
        """Batch delete items into the database table.

        Args:
            items: List of items to be deleted. Each item can be a DynamoDbModel object or a dict.
        """
        with self._table.batch_writer() as batch:
            for key in keys:
                batch.delete_item(Key=key)

    def query(
        self,
        key_condition,
        index_name: str = None,
        as_dict: bool = False,
        size: int = 0,
        filter: dict = None,
        return_count: bool = False,
        projection: str = "",
        names: dict = None,
        consistent_read: bool = False,
        model_type=None,
        sort_desc: bool = False,
        last_eval_key: str = None,
        limit: int = None,
    ) -> QueryResult[T]:
        """Query the table for a specific key condition.

        Args:
            key_condition: simple or composed conditions formed with `boto3.dynamodb.conditions.Key`
            as_dict: True if the returned results should be dictionaries instead of model instances
            size: results count over which fetching should stop
            filter: a simple or composed filter formed using `boto3.dynamodb.conditions.Attr`
            return_count: return the number of elements meeting the criteria
        Results:
            List of records as objects or dictionaries. If `size` is specified, the returned size is
            not equal with `size`, but the page fetching will stop once the fetched size is greater
            than `size`.
            If return_count is true, return the count instead of the records list.
        """
        results = []
        count = 0
        scanned_count = 0
        params = {
            "KeyConditionExpression": key_condition,
            "ConsistentRead": consistent_read
        }

        if limit:
            params["Limit"] = limit

        if index_name:
            params["IndexName"] = index_name

        if sort_desc:
            params["ScanIndexForward"] = False

        if projection:
            params["ProjectionExpression"] = projection
            if names:
                params["ExpressionAttributeNames"] = names

        if filter:
            params["FilterExpression"] = filter

        if not (as_dict or return_count or projection):
            params.update(self._prepare_fetch_fields())

        if return_count:
            params["Select"] = "COUNT"

        if not model_type:
            model_type = self._model_type

        while True:
            if last_eval_key:
                params["ExclusiveStartKey"] = last_eval_key

            db_items = self._table.query(**params)
            scanned_count += db_items.get("ScannedCount", 0)
            last_eval_key = db_items.get("LastEvaluatedKey")

            if return_count:
                count += db_items["Count"]
            else:
                for item in db_items["Items"]:
                    if not as_dict:
                        results.append(model_type(**item))
                    else:
                        results.append(item)

            if not last_eval_key:
                break

            if limit and len(results) >= limit:
                break

            # Don't return when we have the exact size, so we can signal when there are items left
            if size > 0 and len(results) > size:
                break

        return QueryResult(
            count=len(results) if not return_count else count,
            scanned_count=scanned_count,
            items=results
        )

    def scan(
            self, projection: str = "", as_dict: bool = False, filter: ConditionBase = None,
            index_name: str = None, names: dict = None, size: int = 0, return_count: bool = False
    ) -> Union[List[T], int]:
        """Scans entire table and return the filtered items.

        Args:
            projection: fields which should be returned for each record
            as_dict: True if the returned results should be dictionaries instead of model instances
            filter: a simple or composed filter formed using `boto3.dynamodb.conditions.Attr`
            size: results count over which fetching should stop
            return_count: return the number of elements meeting the criteria
        Results:
            List of records as objects or dictionaries. If `size` is specified, the returned size is
            not equal with `size`, but the page fetching will stop once the fetched size is greater
            than `size`.
            If return_count is true, return the count instead of the records list.
        """
        results = []
        count = 0
        params = {"ReturnConsumedCapacity": "TOTAL"}

        if projection:
            params["ProjectionExpression"] = projection
            if names:
                params["ExpressionAttributeNames"] = names
        elif not (as_dict or return_count):
            params.update(self._prepare_fetch_fields())

        if index_name:
            params["IndexName"] = index_name

        if filter:
            params["FilterExpression"] = filter

        if return_count:
            params["Select"] = "COUNT"

        last_eval_key = None

        while True:
            if last_eval_key:
                params["ExclusiveStartKey"] = last_eval_key

            db_items = self._table.scan(**params)
            last_eval_key = db_items.get("LastEvaluatedKey")

            if return_count:
                count += db_items["Count"]
            else:
                for item in db_items["Items"]:
                    if not as_dict:
                        results.append(self._model_type(**item))
                    else:
                        results.append(item)

            if not last_eval_key:
                break

            # Don't return when we have the exact size, so we can signal when there are items left
            if size > 0 and len(results) > size:
                break

        return results if not return_count else count

    def scan_generator(
            self, projection: str = "", as_dict: bool = False, filter: ConditionBase = None,
            names: dict = None, size: int = 0) -> Union[List[T], int]:
        """Scans entire table and return the filtered items as a generator.

        Args:
            projection: fields which should be returned for each record
            as_dict: True if the returned results should be dictionaries instead of model instances
            filter: a simple or composed filter formed using `boto3.dynamodb.conditions.Attr`
            size: results count over which fetching should stop
        Results:
            List of records as objects or dictionaries. If `size` is specified, the returned size is
            not equal with `size`, but the page fetching will stop once the fetched size is greater
            than `size`.
        """
        items_count = 0
        params = {}
        params["ReturnConsumedCapacity"] = "TOTAL"

        if projection:
            params["ProjectionExpression"] = projection
            if names:
                params["ExpressionAttributeNames"] = names
        elif not as_dict:
            params.update(self._prepare_fetch_fields())

        if filter:
            params["FilterExpression"] = filter

        last_eval_key = None

        while True:
            if last_eval_key:
                params["ExclusiveStartKey"] = last_eval_key

            db_items = self._table.scan(**params)
            last_eval_key = db_items.get("LastEvaluatedKey")

            for item in db_items["Items"]:
                items_count += 1
                if not as_dict:
                    yield self._model_type(**item)
                else:
                    yield item

            if not last_eval_key:
                break

            # Don't return when we have the exact size, so we can signal when there are items left
            if size > 0 and items_count > size:
                break


class DynamoDbTransactionTable:
    TRANSACTION_SIZE = 100

    def __init__(self, client, table: DynamodbTable):
        self._table = table
        self._client = client
        self.items: list = []

    def put_item(self, item: DynamoDbModel):
        self.items.append({"type": "Put", "item": item})

    def update_item(self, key: dict, expression: str, values: dict, names: dict = {}):
        self.items.append({
            "type": "Update", "key": key, "expression": expression, "values": values, "names": names
        })

    def delete_item(self, key: dict):
        self.items.append({
            "type": "Delete", "key": key
        })

    def _commit(self):
        if not self.items:
            return

        if len(self.items) == 1:
            item_data = self.items[0]
            if item_data["type"] == "Put":
                return self._table.put_item(item_data["item"])
            elif item_data["type"] == "Delete":
                return self._table.delete_item(item_data["key"])
            elif item_data["type"] == "Update":
                return self._table.update_item(
                    key=item_data["key"],
                    expression=item_data["expression"],
                    values=item_data["values"],
                    names=item_data["names"]
                )
            else:
                raise Exception(f"Unknown DynamoDB operation type {item_data['type']}")

        while True:
            batch_items = self.items[:self.TRANSACTION_SIZE]
            if not batch_items:
                break

            transact_items = []
            self.items = self.items[self.TRANSACTION_SIZE:]

            for item_data in batch_items:
                if item_data["type"] == "Put":
                    transact_items.append({
                        "Put": {
                            "Item": item_data["item"].to_dynamodb_dict(serialize=True),
                            "TableName": self._table._table_name
                        }
                    })

                elif item_data["type"] == "Delete":
                    transact_items.append({
                        "Delete": {
                            "Key": item_data["key"],
                            "TableName": self._table._table_name
                        }
                    })

                elif item_data["type"] == "Update":
                    transact_items.append({
                        "Update": {
                            "Key": item_data["key"],
                            "UpdateExpression": item_data["expression"],
                            "ExpressionAttributeNames": item_data["names"],
                            "ExpressionAttributeValues": item_data["values"],
                            "TableName": self._table._table_name
                        }
                    })

            self._client.transact_write_items(
                TransactItems=transact_items
            )


class DynamoDbTransaction:
    TRANSACTION_SIZE = 100

    def __init__(self, client, *tables: DynamodbTable):
        self.client = client
        self.tables = tuple(DynamoDbTransactionTable(client, table) for table in tables)
        self.partially_commited = False

    def __enter__(self):
        return self.tables

    def __exit__(self, type, value, traceback):
        self.commit()

    def commit(self):
        items = []
        for table in self.tables:
            items.extend({"table": table, "item": item} for item in table.items)

        if not items:
            return

        if len(items) == 1:
            table = items[0]["table"]._table
            item_data = items[0]["item"]

            if item_data["type"] == "Put":
                return table.put_item(item_data["item"])
            elif item_data["type"] == "Delete":
                return table.delete_item(item_data["key"])
            elif item_data["type"] == "Update":
                return table.update_item(
                    key=item_data["key"],
                    expression=item_data["expression"],
                    values=item_data["values"],
                    names=item_data["names"]
                )
            else:
                raise Exception(f"Unknown DynamoDB operation type {item_data['type']}")

        self.partially_commited = False

        while True:
            batch_items = items[:self.TRANSACTION_SIZE]
            if not batch_items:
                break

            transact_items = []
            items = items[self.TRANSACTION_SIZE:]

            transact_items = []

            for item in batch_items:
                table = item["table"]._table
                item_data = item["item"]

                if item_data["type"] == "Put":
                    transact_items.append({
                        "Put": {
                            "Item": item_data["item"].to_dynamodb_dict(serialize=True),
                            "TableName": table._table_name
                        }
                    })

                elif item_data["type"] == "Delete":
                    transact_items.append({
                        "Delete": {
                            "Key": json_util.dumps(item_data["key"], as_dict=True),
                            "TableName": table._table_name
                        }
                    })

                elif item_data["type"] == "Update":
                    attr_values = {}
                    for key, val in item_data["values"].items():
                        if type(val) not in (dict, tuple):
                            attr_values[key] = json_util.dumps([val], as_dict=True)[0]
                        else:
                            value = json_util.dumps(val, as_dict=True)
                            if isinstance(val, dict):
                                value = {"M": value}
                            attr_values[key] = value

                    params = {
                        "Key": json_util.dumps(item_data["key"], as_dict=True),
                        "UpdateExpression": item_data["expression"],
                        "ExpressionAttributeValues": attr_values,
                        "TableName": table._table_name
                    }

                    if item_data.get("names"):
                        params["ExpressionAttributeNames"] = item_data["names"]

                    transact_items.append({
                        "Update": params
                    })

            self.client.transact_write_items(
                TransactItems=transact_items
            )
            self.partially_commited = True

        self.partially_commited = False


class DynamodbCachedTable(Generic[T]):
    CACHE_TIMEOUT = 120

    def __init__(self):
        self._table = None
        self._items = None
        self._timestamp = 0

    def _scan(self):
        raise NotImplementedError("`_scan` should be overwritten")

    def scan(self) -> List[T]:
        if self._items is None or self._timestamp + self.CACHE_TIMEOUT < time.time():
            self._timestamp = time.time()
            self._scan()
        return list(self._items.values())

    def _get_item(self, key: dict) -> T:
        raise NotImplementedError("`_get_item` should be overwritten")

    def _get_items(self, keys: List[dict]) -> List[T]:
        raise NotImplementedError("`_get_items` should be overwritten")

    def get_items(self, keys: List[dict]) -> List[T]:
        key_values = {next(iter(key.values())) for key in keys}
        if not self._items or self._timestamp + self.CACHE_TIMEOUT < time.time():
            self._timestamp = time.time()
            if isinstance(self._items, dict):
                self._items.clear()
            if len(keys) == 1:
                self._get_item(keys[0])
            else:
                self._get_items(keys)
        else:
            missing_items = key_values - self._items.keys()
            if missing_items:
                missing_keys = [key for key in keys if next(iter(key.values())) in missing_items]
                if len(missing_keys) == 1:
                    self._get_item(missing_keys[0])
                else:
                    self._get_items(missing_keys)

        return [self._items[key_value] for key_value in key_values if key_value in self._items]

    def get_item(self, key: dict) -> T:
        result = self.get_items([key])
        return result[0] if result else None
