# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymemuc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymemuc',
    'version': '0.0.3',
    'description': 'A Memuc.exe wrapper for Python',
    'long_description': '# pymemuc\n\nA wrapper for [memuc](https://www.memuplay.com/blog/memucommand-reference-manual.html) in python.\n\nSee [pymemuc.md](docs/pymemuc.md) for package documentation.\n\nSee [memuc_documentation.md](docs/memuc_documentation.md) for a list of all commands.\n',
    'author': 'Martin Miglio',
    'author_email': 'code@martinmiglio.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/marmig0404/pymemuc',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
