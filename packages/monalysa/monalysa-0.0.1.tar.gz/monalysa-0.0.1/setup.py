# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monalysa', 'monalysa.preprocess', 'monalysa.quality', 'monalysa.ulfunc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'monalysa',
    'version': '0.0.1',
    'description': 'A unified library for carrying out quantitative movement analysis.',
    'long_description': '',
    'author': 'Sivakumar Balasubramanian (Siva)',
    'author_email': 'siva82kb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/siva82kb/monalysa',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
