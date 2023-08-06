# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['function_output_monitor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'function-output-monitor',
    'version': '0.1.0',
    'description': 'Watches for a specific function return to change before timeout expires',
    'long_description': '# function-output-monitor\nWatches for a specific function output to change before timeout expires\n',
    'author': 'Gabriel Chamon Araujo',
    'author_email': 'gabriel.chamon@tutanota.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
