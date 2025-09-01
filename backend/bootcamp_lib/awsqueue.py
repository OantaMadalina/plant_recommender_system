import boto3

from bootcamp_lib.logger import Logger


class AWSQueue:

    def __init__(self, queue_url: str, sqs_res=None):
        self._queue_url = queue_url
        self._sqs_res = sqs_res if sqs_res else boto3.resource(
            "sqs", endpoint_url="https://sqs.eu-west-1.amazonaws.com")
        self._queue = self._sqs_res.Queue(self._queue_url)

    def send_message(self, body: str, group_id: str = None, deduplication_id: str = None):
        params = {
            "MessageBody": body
        }

        if group_id:
            params["MessageGroupId"] = group_id

        if deduplication_id:
            params["MessageDeduplicationId"] = deduplication_id
        Logger().debug({
            "SQS action": "sendMessage",
            "Queue": self._queue_url,
            "Parameters": params
        })
        self._queue.send_message(**params)
