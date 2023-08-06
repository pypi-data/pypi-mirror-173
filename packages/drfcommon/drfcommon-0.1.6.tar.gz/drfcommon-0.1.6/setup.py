# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drfcommon']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0',
 'djangorestframework>=3.12.2,<4.0.0',
 'drfhumplib>=0.1.4.1,<0.2.0.0']

setup_kwargs = {
    'name': 'drfcommon',
    'version': '0.1.6',
    'description': 'a common tools for drf',
    'long_description': 'None',
    'author': 'huoyinghui',
    'author_email': 'hyhlinux@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pydtools/drfcommon/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
