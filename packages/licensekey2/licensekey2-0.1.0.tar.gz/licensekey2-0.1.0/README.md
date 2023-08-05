# licensekey2

## Installation

```bash
pip install licensekey2
```

## Usage

### API license keys

Keys is generated and verifyed on the server.

```python
from licensekey2 import RemoteLicense

license = RemoteLicense("https://example.com/api/license")

# Check if the license is valid
license.validate("1234-5678-9012-3456")
```

### Crypto license keys

```python
from datetime import datetime
from licensekey2 import CryptoLicense

# Generate keys. Private key MUST BE kept secret.
public_key, private_key = CryptoLicense.generate_key_pair()
print(public_key, private_key)

# Initialize license object
license = CryptoLicense(public_key, private_key)

# Prepare license subject
license_data = {
    "name": "John Doe",
    "product": "My Product",
    "type": "Ultimate License"
}

# Generate key
key = license.generate_key({}, until=datetime(2025, 1, 1))
print(key)

# Check key and return our license_data
license_subject = license.validate(key)

# Check license type
if license_subject["type"] == "Ultimate License":
    print("You have an ultimate license!")
```

### Custom checkers

```python
def custom_checker(license_subject):
    if license_subject["type"] == "Ultimate License":
        return
    raise ValueError("You don't have an ultimate license!")

license = CryptoLicense(public_key, private_key, custom_checker=custom_checker)

key = license.generate_key({"type": "Ultimate License"}, until=datetime(2025, 1, 1))
license.validate(key)
# Key is valid

key = license.generate_key({"type": "Another license"}, until=datetime(2025, 1, 1))
license.validate(key)
# Key is invalid. ValueError raised.
```

## Authors and license

Licensed under the [MIT license](LICENSE).

First version by Marat Budkevich (@marat2509)

This version by Egor Ternovoy <cofob@riseup.net> (@cofob)
