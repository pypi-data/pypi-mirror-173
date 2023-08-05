# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpleasyncfilestorage']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0', 'aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'simpleasyncfilestorage',
    'version': '0.1.1',
    'description': '',
    'long_description': '# SimpleAsyncFileStorage\nStore files with a uniform API on either your hard-drive or in the deta-cloud.',
    'author': 'Mawoka',
    'author_email': 'git@mawoka.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
