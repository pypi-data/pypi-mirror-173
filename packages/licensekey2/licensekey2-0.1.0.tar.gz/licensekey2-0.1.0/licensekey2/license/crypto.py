from datetime import datetime
from json import dumps, loads
from typing import Callable, Optional, Tuple

from ..exceptions import (
    LicenseKeyExpired,
    LicenseKeyInvalid,
    LicenseKeyInvalidFormat,
)
from ..types import JSONType
from .abstract import AbstractLicense

try:
    import cryptography
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519
except:
    cryptography = None  # type: ignore


class CryptoLicense(AbstractLicense):
    """License verifyer using cryptography signing.

    On client side, only public key must be provided.
    On server/developer side, both public and private keys must be provided.

    It works with JWT-like tokens and doesnt use any external services.

    Main advantage is that it is very fast and does not require any external services.
    Main disadvantage is that key is very big.

    Requires library to be installed with `crypto` extra.
    """

    def __init__(
        self,
        public_key: str,
        private_key: Optional[str] = None,
        custom_checker: Optional[Callable[[JSONType], None]] = None,
    ) -> None:
        """Initialize the license verifyer.

        Args:
            public_key (str): The public key to use to verify the license.
            private_key (str, optional): The private key to use to generate the license. Defaults to None.
            custom_checker (Callable, optional): Custom checker to validate the license. Defaults to None.
        """
        if cryptography is None:
            raise ImportError("cryptography is not installed")
        self.public_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
        self.private_key = (
            ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_key))
            if private_key
            else None
        )
        self.custom_checker = custom_checker

    @staticmethod
    def generate_key_pair() -> Tuple[str, str]:
        """Generate ed25519 key pair.

        Private key **MUST** be kept secret. Public key can be shared.

        Keys in hex format.

        Returns:
            tuple: (public_key, private_key)
        """
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        return (
            public_key.public_bytes(
                encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
            ).hex(),
            private_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            ).hex(),
        )

    def _validate_key(self, subject: bytes, signature: bytes) -> bool:
        try:
            self.public_key.verify(signature, subject)
            return True
        except cryptography.exceptions.InvalidSignature:
            return False

    @staticmethod
    def _parse_key(key: str) -> Tuple[bytes, bytes]:
        try:
            subject, signature = key.split(".")
            return bytes.fromhex(subject), bytes.fromhex(signature)
        except (ValueError, IndexError):
            raise LicenseKeyInvalidFormat("Invalid key format")

    def validate_key(self, key: str) -> bool:
        """Validate the license key.

        Key is in format `{subject}.{signature}`.

        Examples:
            >>> license = CryptoLicense("public_key")
            >>> license.validate_key("1234-5678-9012-3456")
            True

        Args:
            key (str): The license key to validate.
        """
        try:
            subject, signature = key.split(".")
            self._validate_key(bytes.fromhex(subject), bytes.fromhex(signature))
            return True
        except (ValueError, IndexError, cryptography.exceptions.InvalidSignature):
            return False

    def generate_key(  # type: ignore
        self, subject: JSONType, until: datetime, from_date: Optional[datetime] = None
    ) -> str:
        """Generate a license key.

        Args:
            subject (JSONType): The subject of the license.
            until (datetime): The expire date of the license.
            from_date (datetime, optional): The start date of the license. Defaults to None.
        """
        if self.private_key is None:
            raise ValueError("Private key is not provided")
        if from_date is not None and from_date > until:
            raise ValueError("From date must be before until date")
        subject.update(
            {
                "until": int(until.timestamp()),
                "from_date": int(from_date.timestamp()) if from_date else None,
            }
        )
        subject_val = dumps(subject).encode()
        signature = self.private_key.sign(subject_val)
        return f"{subject_val.hex()}.{signature.hex()}"

    @staticmethod
    def _get_subject(subject: bytes) -> JSONType:
        return loads(subject.decode())  # type: ignore

    def get_subject(self, key: str) -> JSONType:
        """Get the subject of the license.

        Args:
            key (str): The license key to get the subject from.
        """
        subject, _ = self._parse_key(key)
        return self._get_subject(subject)

    def validate(self, key: str) -> JSONType:  # type: ignore
        """Validate key.

        Check if key is valid and not expired.

        Examples:
            >>> license = CryptoLicense("public_key")
            >>> license.validate("1234-5678-9012-3456")
            {
                'subject': {'name': 'John Doe'},
                'from_date': datetime.datetime(2020, 1, 1, 0, 0),
                'until': datetime.datetime(2021, 1, 1, 0, 0)
            }

        Args:
            key (str): The license key to validate.

        Returns:
            JSONType: The subject of the license.

        Raises:
            LicenseKeyInvalid: If the key is invalid.
            LicenseKeyExpired: If the key is expired.
            LicenseKeyInvalidFormat: If the key format is invalid.
        """
        subject, signature = self._parse_key(key)
        if not self._validate_key(subject, signature):
            raise LicenseKeyInvalid("Invalid key")
        subject = self._get_subject(subject)
        now = datetime.now()
        if now > datetime.fromtimestamp(subject["until"]):  # type: ignore
            raise LicenseKeyExpired("Key expired")
        if subject["from_date"] is not None and now < datetime.fromtimestamp(subject["from_date"]):  # type: ignore
            raise LicenseKeyInvalid("Key not valid yet")
        if self.custom_checker:
            self.custom_checker(subject)
        return subject
