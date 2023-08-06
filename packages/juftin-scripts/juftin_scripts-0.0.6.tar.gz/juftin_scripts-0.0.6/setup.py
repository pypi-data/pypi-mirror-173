# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['juftin_scripts']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'rich-click>=1.5.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'textual>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['browse = juftin_scripts.code_browser:main',
                     'rotate-aws-profile = juftin_scripts.rotation:rotate']}

setup_kwargs = {
    'name': 'juftin-scripts',
    'version': '0.0.6',
    'description': 'Helpful Python scripts by @juftin',
    'long_description': '# juftin-scripts\n\nHelpful Python scripts by @juftin\n\n#### Check Out the [Docs](https://juftin.github.io/juftin-scripts/)\n#### Looking to contribute? See the [Contributing Guide](docs/source/contributing.md)\n#### See the [Changelog](https://github.com/juftin/juftin-scripts/releases)\n\n___________\n___________\n\n<br/>\n\n<p align="center"><a href="https://github.com/juftin"><img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120" alt="logo"></p>\n',
    'author': 'Justin Flannery',
    'author_email': 'juftin@juftin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/juftin/juftin-scripts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
