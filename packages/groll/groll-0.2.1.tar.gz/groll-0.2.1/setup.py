# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['groll']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['groll = groll.groll:app']}

setup_kwargs = {
    'name': 'groll',
    'version': '0.2.1',
    'description': 'A helpful diceroller for your command line!',
    'long_description': '# Groll\n\n*A helpful diceroller for your command line!*\n\n## Installation\n\n```\npip install groll\n```\n\n## Usage\n\n```\ngroll [Options] DICE...\n\nOptions:\n--version             -v        Print version and exit.\n--long                -l        Show rolled values in ouput.\n--install-completion            Install completion for the current shell.\n--show-completion               Show completion for the current shell, to copy it or customize the installation.\n--help                          Show this message and exit.\n```\n\nGroll parses user input for dice notation and evaluates the resulting expression. At its most basic, it can be used to roll a (virtual) handful of dice:\n\n```bash\n$ groll 2d6\n> 5\n```\n\nIt can also handle modifiers in the input:\n\n```bash\n$ groll d20 + 4\n> 11\n```\n\nMore complicated expressions are possible by wrapping input with quotes:\n\n```bash\n$ groll -l "(2d6 + 3) / 2"\n> ((3 + 5) + 3) / 2 -> 5\n```\n',
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
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
