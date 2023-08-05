# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['licensekey2', 'licensekey2.license']

package_data = \
{'': ['*']}

extras_require = \
{'crypto': ['cryptography>=38,<39'], 'requests': ['requests>=2.28,<3.0']}

setup_kwargs = {
    'name': 'licensekey2',
    'version': '0.1.0',
    'description': 'Licensing library',
    'long_description': '# licensekey2\n\n## Installation\n\n```bash\npip install licensekey2\n```\n\n## Usage\n\n### API license keys\n\nKeys is generated and verifyed on the server.\n\n```python\nfrom licensekey2 import RemoteLicense\n\nlicense = RemoteLicense("https://example.com/api/license")\n\n# Check if the license is valid\nlicense.validate("1234-5678-9012-3456")\n```\n\n### Crypto license keys\n\n```python\nfrom datetime import datetime\nfrom licensekey2 import CryptoLicense\n\n# Generate keys. Private key MUST BE kept secret.\npublic_key, private_key = CryptoLicense.generate_key_pair()\nprint(public_key, private_key)\n\n# Initialize license object\nlicense = CryptoLicense(public_key, private_key)\n\n# Prepare license subject\nlicense_data = {\n    "name": "John Doe",\n    "product": "My Product",\n    "type": "Ultimate License"\n}\n\n# Generate key\nkey = license.generate_key({}, until=datetime(2025, 1, 1))\nprint(key)\n\n# Check key and return our license_data\nlicense_subject = license.validate(key)\n\n# Check license type\nif license_subject["type"] == "Ultimate License":\n    print("You have an ultimate license!")\n```\n\n### Custom checkers\n\n```python\ndef custom_checker(license_subject):\n    if license_subject["type"] == "Ultimate License":\n        return\n    raise ValueError("You don\'t have an ultimate license!")\n\nlicense = CryptoLicense(public_key, private_key, custom_checker=custom_checker)\n\nkey = license.generate_key({"type": "Ultimate License"}, until=datetime(2025, 1, 1))\nlicense.validate(key)\n# Key is valid\n\nkey = license.generate_key({"type": "Another license"}, until=datetime(2025, 1, 1))\nlicense.validate(key)\n# Key is invalid. ValueError raised.\n```\n\n## Authors and license\n\nLicensed under the [MIT license](LICENSE).\n\nFirst version by Marat Budkevich (@marat2509)\n\nThis version by Egor Ternovoy <cofob@riseup.net> (@cofob)\n',
    'author': 'Egor Ternovoy',
    'author_email': 'cofob@riseup.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.frsqr.xyz/cofob/license-key',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
