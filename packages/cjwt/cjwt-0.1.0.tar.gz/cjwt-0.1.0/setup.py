# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjwt']

package_data = \
{'': ['*']}

install_requires = \
['pyjwt>=2.6.0,<3.0.0']

entry_points = \
{'console_scripts': ['cjwt = cjwt.__main__:main']}

setup_kwargs = {
    'name': 'cjwt',
    'version': '0.1.0',
    'description': 'Simple JWT reader utility',
    'long_description': "# Cat JWT\n\n## Usage\n\n```\nusage: cjwt [-h] [--secret [SECRET]] [file]\n\npositional arguments:\n  file\n\noptions:\n  -h, --help         show this help message and exit\n  --secret [SECRET]  JWT secret\n```\n\n## Examples\n\n### Read header and claims\n\n```\necho 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0ZXN0IjoiYWJjZGVmIn0.tPJ7bVKyF_FMFQaRT6n7dvhEBnyiBRGhVlwacTsy0mI' | cjwt\nalg: HS256\ntyp: JWT\nsub: 1234567890\nname: John Doe\niat: 1516239022\ntest: abcdef\n```\n\n```\ncjwt /tmp/jwt.txt\nalg: HS256\ntyp: JWT\nsub: 1234567890\nname: John Doe\niat: 1516239022\ntest: abcdef\n```\n\n### Verify secret\n\n```\necho 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0ZXN0IjoiYWJjZGVmIn0.tPJ7bVKyF_FMFQaRT6n7dvhEBnyiBRGhVlwacTsy0mI' | cjwt --secret 'secret'\nalg: HS256\ntyp: JWT\nsub: 1234567890\nname: John Doe\niat: 1516239022\ntest: abcdef\n```\n\n```\necho 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0ZXN0IjoiYWJjZGVmIn0.tPJ7bVKyF_FMFQaRT6n7dvhEBnyiBRGhVlwacTsy0mI' | cjwt --secret 'not-secret'\nalg: HS256\ntyp: JWT\nSignature verification failed\n```\n",
    'author': 'Max Harley',
    'author_email': 'maxh@maxh.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
