import logging
from unittest.mock import patch

from app.core.security import PIIMasker, SecureLogger


class TestPIIMasking:
    def test_mask_email(self) -> None:
        """Test that email addresses are properly masked"""
        text = "Contact user@example.com for details"
        masked = PIIMasker.mask_email(text)
        assert "user@example.com" not in masked
        assert "[EMAIL_REDACTED]" in masked

    def test_mask_phone(self) -> None:
        """Test that phone numbers are properly masked"""
        text = "Call +7 (123) 456-78-90"
        masked = PIIMasker.mask_phone(text)
        assert "+7 (123) 456-78-90" not in masked
        assert "[PHONE_REDACTED]" in masked

    def test_mask_ip(self) -> None:
        """Test that IP addresses are properly masked"""
        text = "From IP 192.168.1.1"
        masked = PIIMasker.mask_ip(text)
        assert "192.168.1.1" not in masked
        assert "[IP_REDACTED]" in masked

    def test_mask_all_pii(self) -> None:
        """Test that all PII types are masked together"""
        text = "User user@test.com from 192.168.1.1 called +79991234567"
        masked = PIIMasker.mask_all_pii(text)
        assert "user@test.com" not in masked
        assert "192.168.1.1" not in masked
        assert "+79991234567" not in masked
        assert "[EMAIL_REDACTED]" in masked
        assert "[IP_REDACTED]" in masked
        assert "[PHONE_REDACTED]" in masked

    def test_mask_multiple_emails(self) -> None:
        """Test masking multiple email addresses"""
        text = "Contacts: admin@site.com and user@domain.org"
        masked = PIIMasker.mask_all_pii(text)
        assert "admin@site.com" not in masked
        assert "user@domain.org" not in masked
        assert masked.count("[EMAIL_REDACTED]") == 2

    def test_no_pii_unchanged(self) -> None:
        """Test that text without PII remains unchanged"""
        text = "This is a normal log message without sensitive data"
        masked = PIIMasker.mask_all_pii(text)
        assert masked == text

    def test_mixed_content(self) -> None:
        """Test masking in mixed content"""
        text = "User with email test@example.com and IP 10.0.0.1 performed action"
        masked = PIIMasker.mask_all_pii(text)
        assert "test@example.com" not in masked
        assert "10.0.0.1" not in masked
        assert "[EMAIL_REDACTED]" in masked
        assert "[IP_REDACTED]" in masked

    def test_secure_logger_masks_pii(self) -> None:
        """Test that SecureLogger automatically masks PII in log messages"""
        logger = SecureLogger("test_logger")

        with patch.object(logging.Logger, "log") as mock_log:
            logger.warning("User user@example.com from 192.168.1.1 called")

            mock_log.assert_called_once()
            call_args = mock_log.call_args[0]
            log_message = call_args[1]

            assert "user@example.com" not in log_message
            assert "192.168.1.1" not in log_message
            assert "[EMAIL_REDACTED]" in log_message
            assert "[IP_REDACTED]" in log_message
