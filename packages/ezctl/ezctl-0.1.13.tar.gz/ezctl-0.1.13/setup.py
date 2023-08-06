# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commands', 'commons', 'ezctl']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ezctl = ezctl.main:app']}

setup_kwargs = {
    'name': 'ezctl',
    'version': '0.1.13',
    'description': '',
    'long_description': '# ezctl\n\nintegrate sp/ssp/pbf to start a local nbroute',
    'author': 'peijia',
    'author_email': 'peijia@nextbillion.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
