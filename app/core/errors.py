class AppError(Exception):
    def __init__(self, code: str, msg: str, status: int = 400):
        self.code = code
        self.msg = msg
        self.status = status
