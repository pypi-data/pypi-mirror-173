import boto3
import json
from factoree_ai_connectors.files.file_types import S3TextFile, S3FileCreatedEvent
from logging import Logger


class S3SourceConnector:
    event_list: list[S3FileCreatedEvent] = []
    current_file = None

    def __init__(
            self,
            region_name: str,
            sqs_url: str,
            aws_access_key: str,
            aws_secret_key: str,
            logger: Logger
    ):
        self.sqs_url = sqs_url
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

        self.sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=region_name
        )
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=region_name
        )
        self.logger = logger

    def next_created_file_event(self) -> S3FileCreatedEvent | None:
        # TODO: error handling
        self.logger.info(f'Getting events from {self.sqs_url}')
        response = self.sqs_client.receive_message(
            QueueUrl=self.sqs_url,
            MaxNumberOfMessages=1,
        )
        event: S3FileCreatedEvent = self.__get_file_created_event_from_response(response)
        if event is None:
            self.logger.info('No messages in queue')
        else:
            self.logger.info(f'Received message of new file {event.filename}')

        return event

    def __get_file_created_event_from_response(self, response) -> S3FileCreatedEvent | None:
        event: S3FileCreatedEvent | None = None
        for message in response.get('Messages', []):
            handler = message.get('ReceiptHandle', '')
            try:
                body_str = message.get('Body')
                body_json = json.loads(body_str)
                for record in body_json.get('Records', []):
                    filename = record.get('s3', {}).get('object', {}).get('key')
                    bucket_name = record.get('s3', {}).get('bucket', {}).get('name', '')
                    event = S3FileCreatedEvent(bucket_name, filename, handler)
            except IndexError or TypeError as e:
                self.logger.error(str(e))

        return event

    def fetch_s3_file(self, bucket_name: str, file_key: str) -> S3TextFile:
        data: str = self.__read_file_content_from_s3(bucket_name, file_key)
        return S3TextFile(bucket_name, file_key, data)

    def purge_events(self):
        self.sqs_client.purge_queue(QueueUrl=self.sqs_url)

    def __read_file_content_from_s3(self, bucket_name: str, s3_path: str) -> str:
        data = self.s3_client.get_object(Bucket=bucket_name, Key=s3_path)
        return data['Body'].read().decode('UTF-8')

    def mark_file_as_done(self, file_id: str) -> bool:
        # TODO: error handling
        self.logger.info(f'Deleting message {file_id} from queue')
        self.sqs_client.delete_message(
            QueueUrl=self.sqs_url,
            ReceiptHandle=file_id
        )
        return True
