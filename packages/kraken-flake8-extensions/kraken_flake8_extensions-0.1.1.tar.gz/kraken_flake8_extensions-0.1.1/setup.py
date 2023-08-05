# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kraken_flake8_extensions', 'kraken_flake8_extensions.kraken']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8.1,<0.9.0']

entry_points = \
{'flake8.extension': ['KRE = '
                      'kraken_flake8_extensions.kraken:Flake8KrakenPlugin']}

setup_kwargs = {
    'name': 'kraken-flake8-extensions',
    'version': '0.1.1',
    'description': '',
    'long_description': '# kraken-flake8-extensions\n\nThis Flake8 plugin implements lints specific for the code base of the Kraken build system.\n\n| Code | Description |\n| ---- | ----------- |\n| `KRE001` | Annotations on `kraken.core.property.Object` subclasses (such as tasks) must use backwards compatible type hints because they are evaluated at runtime. Use collection types from the `typing` module instead. |\n| `KRE002` | Use of built-in type subscripts (3.9+) or type unions (3.10+) requires `from __future__ import annotations` for backwards compatibility. |\n',
    'author': 'Unknown',
    'author_email': 'me@unknown.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
