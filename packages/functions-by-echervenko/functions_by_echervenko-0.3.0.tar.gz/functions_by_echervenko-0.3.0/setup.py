# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functions_by_echervenko']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'functions-by-echervenko',
    'version': '0.3.0',
    'description': 'This is our test project',
    'long_description': '# Instructions\n\n#### This is our test project.\n\n#### Please istall this package \n\n```\npip install functions-by-echervenko\n```\n\n#### You can also install older package\n```\npip install functions-by-echervenko==VERSION_NUMBER\n```',
    'author': 'Elena Chervenko',
    'author_email': 'echervenko@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
