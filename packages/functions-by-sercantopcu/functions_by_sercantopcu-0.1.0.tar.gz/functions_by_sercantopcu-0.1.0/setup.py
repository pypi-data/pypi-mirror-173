# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functions_by_sercantopcu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'functions-by-sercantopcu',
    'version': '0.1.0',
    'description': 'This is our test project',
    'long_description': '',
    'author': 'somename',
    'author_email': 'sercantopcu1@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
