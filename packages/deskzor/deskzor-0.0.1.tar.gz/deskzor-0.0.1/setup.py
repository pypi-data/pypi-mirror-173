# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deskzor',
 'deskzor.api',
 'deskzor.api.metadata',
 'deskzor.core',
 'deskzor.models',
 'deskzor.models.metadata']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'piou>=0.10.5,<1.0', 'pydantic>=1.9.2,<2.0.0']

entry_points = \
{'console_scripts': ['cli = run:run']}

setup_kwargs = {
    'name': 'deskzor',
    'version': '0.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'abonur',
    'author_email': 'sm7.abonur@gmail.com',
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
