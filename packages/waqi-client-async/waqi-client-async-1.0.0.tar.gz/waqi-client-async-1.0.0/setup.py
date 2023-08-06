# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['waqi_client_async']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'waqi-client-async',
    'version': '1.0.0',
    'description': 'An asynchronous client to query data from the World Air Quality Index project (aqicn.org, waqi.info).',
    'long_description': '### Asynchronous WAQI client\nThis module allows to query data from the\n[World Air Quality Index](http://waqi.info/) project.\n',
    'author': 'Stanislas Bach',
    'author_email': 'sbach@0g.re',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbach/waqi-client-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
