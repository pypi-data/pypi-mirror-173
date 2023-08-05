# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['views_dataviz', 'views_dataviz.map', 'views_dataviz.map.presets']

package_data = \
{'': ['*'], 'views_dataviz.map': ['assets/*']}

install_requires = \
['adjustText>=0.7.3,<0.8.0',
 'contextily>=1.1.0,<2.0.0',
 'geopandas>=0.11.0,<0.12.0',
 'ipykernel>=6.15.1,<7.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'pandas>=1.4.3,<2.0.0',
 'seaborn>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'views-dataviz',
    'version': '0.10.0',
    'description': '',
    'long_description': 'None',
    'author': 'mihai',
    'author_email': 'mihai.croicu@pcr.uu.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
