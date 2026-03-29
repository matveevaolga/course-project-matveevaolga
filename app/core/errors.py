from app.core.security import secure_logger


class AppError(Exception):
    def __init__(self, code: str, msg: str, status: int = 400):
        self.code = code
        self.msg = msg
        self.status = status
        secure_logger.warning(f"AppError: {code} (status: {status}) - Message: {msg}")
