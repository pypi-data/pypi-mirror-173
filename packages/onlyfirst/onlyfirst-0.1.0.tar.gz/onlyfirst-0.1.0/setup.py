# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onlyfirst']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['olf = onlyfirst.__main__:main']}

setup_kwargs = {
    'name': 'onlyfirst',
    'version': '0.1.0',
    'description': 'only first word remains',
    'long_description': None,
    'author': 'svtter',
    'author_email': 'svtter@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
