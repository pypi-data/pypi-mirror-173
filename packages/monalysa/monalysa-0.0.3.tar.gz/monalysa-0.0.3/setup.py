# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monalysa', 'monalysa.preprocess', 'monalysa.quality', 'monalysa.ulfunc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'monalysa',
    'version': '0.0.3',
    'description': 'A unified library for carrying out quantitative movement analysis.',
    'long_description': '# Monalysa\n** Still Under Development. Please check after some time.** \n\nMonalysa or **Mo**vement A**naly**sis Libr**a**ry is a unified python library for quantifying movement behavior.\n\n## Purpose of the Package\nThis is a single library with a set of data structures, functions, and classes required for quantifying and anlaysing movement behavior for applications in motor control/learning, biomechanics, sports science, and neurorehabilitation.\n\n## Features\nCollection of supported operations:\n    - Movement preprocessing\n    - Movement segmentation \n    - Movement quality\n    - UL functioning\n\n## Getting Started\nYou can install this library using pip.\n```bash\npip install monalysa\n```\n\n## Usage\nComing soon.\n\n## Documentation\nComing soon.\n\n## Authors\nSivakumar Balasubramanian, CMC Vellore\n\nAlejandro Melendex-Calderon, Univ. of Queesland\n\n',
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
