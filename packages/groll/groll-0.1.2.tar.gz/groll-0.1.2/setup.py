# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['groll']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['groll = groll.groll:app']}

setup_kwargs = {
    'name': 'groll',
    'version': '0.1.2',
    'description': 'A helpful diceroller for your command line!',
    'long_description': '# Groll\n\n*A dice roller for your command line!*\n',
    'author': 'Gage Talbot',
    'author_email': 'gagetalbot@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Krognak/groll',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
