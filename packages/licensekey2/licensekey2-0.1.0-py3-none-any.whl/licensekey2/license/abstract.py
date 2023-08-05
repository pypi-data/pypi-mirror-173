from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Optional

from ..types import JSONType


class AbstractLicense(ABC):
    """Abstract class for license verifyers."""

    @abstractmethod
    def __init__(
        self, custom_checker: Optional[Callable[[JSONType], None]], *args, **kwargs
    ) -> None:
        """Initialize the license verifyer."""
        pass

    @abstractmethod
    def validate_key(self, key: str) -> bool:
        """Validate the license key.

        Examples:
            >>> license = AbstractLicense()
            >>> license.validate_key("1234-5678-9012-3456")
            True

        Args:
            key (str): The license key to validate.

        Returns:
            bool: True if the license key is valid, False otherwise.
        """
        pass

    @abstractmethod
    def generate_key(
        self,
        subject: JSONType,
        until: datetime,
        from_date: Optional[datetime] = None,
        *args,
        **kwargs,
    ) -> str:
        """Generate a license key.

        Examples:
            >>> license = AbstractLicense()
            >>> license.generate_key({"name": "John Doe"}, datetime(2020, 1, 1))
            "1234-5678-9012-3456"

        Args:
            subject (dict): The subject of the license. Example: `{"name": "John Doe", "type": "pro"}`.
            until (datetime): The expiration date of the license key.
            from_date (datetime, optional): The date from which the license key is valid. Defaults to None.

        Returns:
            str: The generated license key.
        """
        pass

    @abstractmethod
    def get_subject(self, key: str) -> JSONType:
        """Get the subject of the license key.

        Examples:
            >>> license = AbstractLicense()
            >>> license.get_subject("1234-5678-9012-3456")
            {"name": "John Doe", "type": "pro"}

        Args:
            key (str): The license key to get the subject from.

        Returns:
            dict: The subject of the license key.

        Raises:
            LicenseKeyInvalidKey: If the license key is invalid.
        """
        pass

    @abstractmethod
    def validate(self, key: str, *args, **kwargs) -> JSONType:
        """Validate the license key.

        Validation includes:
        - Checking if the key is valid format.
        - Checking if the key is valid signature.
        - Checking if the key is expired.

        Examples:
            >>> license = AbstractLicense()
            >>> license.validate("1234-5678-9012-3456")
            True

        Args:
            key (str): The license key to validate.

        Returns:
            dict: The subject of the license key.

        Raises:
            LicenseKeyInvalidKey: If the license key is invalid.
        """
        pass
