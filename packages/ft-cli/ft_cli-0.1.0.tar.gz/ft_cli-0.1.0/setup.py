# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ft_cli']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ft-cli = ft_cli.main:app']}

setup_kwargs = {
    'name': 'ft-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'wanqiang.liu',
    'author_email': 'wanqiang.liu@freetech.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
