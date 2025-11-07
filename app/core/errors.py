import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AppError(Exception):
    def __init__(self, code: str, msg: str, status: int = 400):
        self.code = code
        self.msg = msg
        self.status = status
        logger.warning(f"AppError: {code} (status: {status})")
