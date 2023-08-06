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
    'version': '1.2.0',
    'description': 'A toy module to generate a map and find the shortest path from two points on the map',
    'long_description': '# kiri-pathfinding\n\n![PythonVersion](https://img.shields.io/badge/python-3.*-blue)\n![PyPi](https://img.shields.io/pypi/v/kiri-pathfinding)\n\n\nA toy module to generate a map and find the shortest path from two points on the map\n\n## Usage\n\n```python\nfrom matplotlib import pyplot as plt\nfrom kiri_pathfinding.map_generator import generate_map, draw_map\nfrom kiri_pathfinding.pathfinding import PathFinding, draw_path\n\n# genetate a map and find shortest path\ndata_map = generate_map(20, 20)\npathfinding = PathFinding(data_map)\npath = pathfinding.find((0, 0), (19, 19))\n\n# visualize\nfig, ax = plt.subplots()\ndraw_map(data_map, ax)\ndraw_path(path, ax)\n```\n\n## Example\n\n![example](example.png)\n\nThe image above visualizes the generated map and the found path from point (0, 0) to point (19, 19).\n\nDifferent colors on the map mean different terrains. \nSpecifically, the green is grassland \nand the gray means roads, providing a lower movement cost. \nThe brown and blue denote mud and river respectively, which are harder to pass.\n',
    'author': 'anthony',
    'author_email': 'mrchowpoor@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kiri-chow/kiri-pathfinding',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
