# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drfcommon']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<4.0', 'djangorestframework>=3.12.2,<4.0.0']

setup_kwargs = {
    'name': 'drfcommon',
    'version': '0.1.8.6',
    'description': 'a common tools for drf',
    'long_description': 'None',
    'author': 'tplinux',
    'author_email': 'tplinux@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pydtools/drfcommon/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
