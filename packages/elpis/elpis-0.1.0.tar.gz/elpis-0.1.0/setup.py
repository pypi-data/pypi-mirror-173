# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elpis',
 'elpis.datasets',
 'elpis.models',
 'elpis.trainer',
 'elpis.transcriber',
 'elpis.utils']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.6.1,<3.0.0',
 'librosa>=0.9.2,<0.10.0',
 'loguru>=0.6.0,<0.7.0',
 'pedalboard>=0.6.2,<0.7.0',
 'pympi-ling>=1.70.2,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'transformers>=4.23.1,<5.0.0']

setup_kwargs = {
    'name': 'elpis',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Harry Keightley',
    'author_email': 'harrykeightley@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
