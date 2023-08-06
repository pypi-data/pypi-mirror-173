# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anno3d',
 'anno3d.annofab',
 'anno3d.annofab.specifiers',
 'anno3d.kitti',
 'anno3d.model',
 'anno3d.util']

package_data = \
{'': ['*']}

install_requires = \
['annofabapi>=0.62.0',
 'boto3>=1.17.20,<2.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'fire>=0.3.1,<0.4.0',
 'more-itertools>=8.5.0,<9.0.0',
 'numpy>=1.23.0,<2.0.0',
 'scipy>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['anno3d = anno3d.app:main']}

setup_kwargs = {
    'name': 'annofab-3dpc-editor-cli',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'Kurusugawa Computer Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
