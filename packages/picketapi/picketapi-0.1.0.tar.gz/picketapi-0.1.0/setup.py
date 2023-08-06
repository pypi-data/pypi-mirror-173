# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['picketapi']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'picketapi',
    'version': '0.1.0',
    'description': 'The official Python library for the Picket API (https://picketapi.com/)',
    'long_description': '# picket-python\n\nThe official Python library for the Picket API\n\n',
    'author': 'Devin Stein',
    'author_email': 'devstein@seas.upenn.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
