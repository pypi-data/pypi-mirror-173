# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymyplot']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'pymyplot',
    'version': '0.0.2',
    'description': 'Correction of usefull plotting setup for matplotlib',
    'long_description': None,
    'author': 'Kyoungseoun Chung',
    'author_email': 'kchung@student.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
