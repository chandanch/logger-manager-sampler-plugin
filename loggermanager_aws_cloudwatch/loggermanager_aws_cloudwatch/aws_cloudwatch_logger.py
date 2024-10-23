from loggermanager import LoggerInterface
import boto3
import logging
import watchtower
import os


class AWSCloudWatchLogger(LoggerInterface):
    def __init__(
        self,
        log_group: str,
        region_name: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
    ):
        self.log_group = log_group
        self.region_name = region_name or os.getenv("AWS_REGION")
        self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.getenv(
            "AWS_SECRET_ACCESS_KEY"
        )

        if (
            not self.region_name
            or not self.aws_access_key_id
            or not self.aws_secret_access_key
        ):
            raise ValueError("AWS credentials and region must be provided.")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = watchtower.CloudWatchLogHandler(
            log_group=self.log_group,
            boto3_session=boto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name,
            ),
        )
        self.logger.addHandler(handler)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_error(self, message: str):
        self.logger.error(message)
