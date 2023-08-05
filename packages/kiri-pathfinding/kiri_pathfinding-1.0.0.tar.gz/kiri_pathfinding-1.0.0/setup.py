# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiri_pathfinding']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.1,<4.0.0',
 'numba>=0.56.3,<0.57.0',
 'numpy>=1.23.4,<2.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'kiri-pathfinding',
    'version': '1.0.0',
    'description': 'A toy module to generate a map and find the shortest path from two points on the map',
    'long_description': 'None',
    'author': 'anthony',
    'author_email': 'mrchowpoor@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
