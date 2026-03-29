import logging
import re
from typing import Any


class PIIMasker:
    """Маскировщик персональных данных в логах"""

    @staticmethod
    def mask_email(text: str) -> str:
        """Маскирует email адреса"""
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.sub(email_pattern, "[EMAIL_REDACTED]", text)

    @staticmethod
    def mask_phone(text: str) -> str:
        """Маскирует номера телефонов"""
        phone_pattern = r"(\+?7|8)?\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
        return re.sub(phone_pattern, "[PHONE_REDACTED]", text)

    @staticmethod
    def mask_ip(text: str) -> str:
        """Маскирует IP адреса"""
        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        return re.sub(ip_pattern, "[IP_REDACTED]", text)

    @staticmethod
    def mask_all_pii(text: str) -> str:
        """Применяет все маскировки PII"""
        text = PIIMasker.mask_email(text)
        text = PIIMasker.mask_phone(text)
        text = PIIMasker.mask_ip(text)
        return text


class SecureLogger:
    """Безопасный логгер с маскировкой PII"""

    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)

    def safe_log(self, level: int, message: str, *args: Any, **kwargs: Any) -> None:
        """Безопасное логирование с маскировкой PII"""
        safe_message = PIIMasker.mask_all_pii(str(message))

        # Маскируем также аргументы
        safe_args = [
            PIIMasker.mask_all_pii(str(arg)) if isinstance(arg, str) else arg
            for arg in args
        ]

        # Форматируем сообщение с безопасными аргументами
        if safe_args:
            try:
                formatted_message = safe_message % tuple(safe_args)
            except (TypeError, ValueError):
                formatted_message = (
                    safe_message + " " + " ".join(str(arg) for arg in safe_args)
                )
        else:
            formatted_message = safe_message

        self.logger.log(level, formatted_message)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.safe_log(logging.INFO, message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.safe_log(logging.WARNING, message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.safe_log(logging.ERROR, message, *args, **kwargs)


secure_logger = SecureLogger(__name__)
