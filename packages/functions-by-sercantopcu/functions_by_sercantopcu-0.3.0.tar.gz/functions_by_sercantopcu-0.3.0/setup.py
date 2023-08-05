# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functions_by_sercantopcu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'functions-by-sercantopcu',
    'version': '0.3.0',
    'description': 'This is our test project',
    'long_description': '# Instructions\n\n#### This is our test project. \n\n#### Please install this package\n```\npip install functions-by-sercantopcu\n```\n\n\n#### You can also install older packages\n```\npip install functions-by-sercantopcu==VERSION_NUMBER\n```',
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
