class LicenseKeyException(Exception):
    """Base class for all exceptions raised by licensekey2 library."""

    pass


class LicenseKeyInvalid(LicenseKeyException):
    """Invalid key."""

    pass


class LicenseKeyExpired(LicenseKeyException):
    """Expired key."""

    pass


class LicenseKeyInvalidFormat(LicenseKeyInvalid):
    """Invalid key format."""

    pass
