# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyvis']

package_data = \
{'': ['*'], 'jrpyvis': ['data/*', 'solutions/*']}

install_requires = \
['matplotlib>=3.5.3,<4.0.0',
 'numpy>=1.23.2,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'jrpyvis',
    'version': '1.0.0',
    'description': 'Jumping Rivers: Data Visualisation with Python',
    'long_description': 'None',
    'author': 'Jumping Rivers',
    'author_email': 'info@jumpingrivers.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
