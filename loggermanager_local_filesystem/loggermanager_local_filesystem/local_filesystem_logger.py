from loggermanager import LoggerInterface
import logging
import os


class LocalFileSystemLogger(LoggerInterface):
    def __init__(self, log_file_path: str = None):
        self.log_file_path = (
            log_file_path or os.getenv("LOCAL_LOG_FILE_PATH") or "fabrikam.log"
        )

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        fh = logging.FileHandler(self.log_file_path)
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_error(self, message: str):
        self.logger.error(message)
