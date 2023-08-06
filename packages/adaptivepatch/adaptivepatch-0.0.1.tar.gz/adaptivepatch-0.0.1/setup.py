# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adaptivepatch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1,<2']

setup_kwargs = {
    'name': 'adaptivepatch',
    'version': '0.0.1',
    'description': 'A library that can split the image into different patches with the optimal step in order to avoid pixel loss.',
    'long_description': '# adaptivepatch\nadaptivepatch can split the image in different patches with automatic detection of the best step in order to do not lose pixels. The overlap between patches depends on the patch size. \n\n## Example\n![pic](example.png)\n\n## Installation\n```Python\npip install adaptivepatch\n```\n## How to use it\n`adaptivepatch(image, patch_size, step=None, verbose)`\n\n## Licence\nMIT Licence\n\n',
    'author': 'Luca Pavirani',
    'author_email': 'luca481998@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LucaPavirani/adaptivepatch.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
