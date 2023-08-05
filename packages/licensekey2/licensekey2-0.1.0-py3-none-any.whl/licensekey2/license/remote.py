from datetime import datetime
from typing import Callable, Optional

from licensekey2.exceptions import LicenseKeyInvalid
from licensekey2.types import JSONType

from .abstract import AbstractLicense

try:
    import requests
except ImportError:
    requests = None  # type: ignore


class RemoteLicense(AbstractLicense):
    """Remote license verifyer.

    It does not support generating keys or getting the subject of a key.
    Server must check the key by itself (like expire date) and return a 200 status code if the key is valid.

    It will make a request to a remote server to `{remote_url}/{key}` to validate.
    If response is 200, the key is valid, otherwise it is not.

    Requires library to be installed with `requests` extra.
    """

    def __init__(
        self,
        remote_url: str,
        scheme: str = "{remote_url}/{key}",
        custom_checker: Optional[Callable[[JSONType], None]] = None,
    ) -> None:
        """Initialize the license verifyer.

        Args:
            remote_url (str): The remote url to make the request to.
            scheme (str, optional): The scheme to use to make the request. Defaults to "{remote_url}/{key}".
        """
        if requests is None:
            raise ImportError("requests is not installed")
        self.remote_url = remote_url
        self.scheme = scheme
        if custom_checker:
            raise ValueError("RemoteLicense does not support custom checker")

    def validate_key(self, key: str) -> bool:
        """Validate the license key.

        Examples:
            >>> license = RemoteLicense("https://example.com")
            >>> license.validate_key("1234-5678-9012-3456")
            True

        Args:
            key (str): The license key to validate.
        """
        r = requests.get(self.scheme.format(remote_url=self.remote_url, key=key))
        if r.status_code == 200:
            return True
        return False

    def validate(self, key: str) -> JSONType:  # type: ignore
        """Validate the license key.

        Proxy to `validate_key`, as RemoteLicense does not support getting the subject of a key.

        Examples:
            >>> license = RemoteLicense("https://example.com")
            >>> license.validate("1234-5678-9012-3456")
            {}
            >>> license.validate("1234^647328fDHSFS&6")
            exception LicenseKeyInvalid

        Args:
            key (str): The license key to validate.

        Returns:
            dict: Empty dict.

        Raises:
            LicenseKeyInvalid: If the license key is invalid.
        """
        if self.validate_key(key):
            return {}
        raise LicenseKeyInvalid("Invalid key")

    def generate_key(  # type: ignore
        subject: JSONType, until: datetime, from_date: Optional[datetime] = None
    ) -> str:
        """Not implemented."""
        raise NotImplementedError("RemoteLicense does not support generating keys")

    def get_subject(self, key: str) -> JSONType:
        """Not implemented."""
        raise NotImplementedError("RemoteLicense does not support getting subject")
