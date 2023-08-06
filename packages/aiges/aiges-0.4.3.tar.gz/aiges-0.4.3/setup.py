# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiges',
 'aiges.backup',
 'aiges.cmd',
 'aiges.core',
 'aiges.examples.once.mmocr',
 'aiges.examples.stream.mmocr',
 'aiges.examples.stream.mock',
 'aiges.utils']

package_data = \
{'': ['*'], 'aiges': ['test_data/*', 'tpls/*']}

install_requires = \
['jinja2>=2.0']

setup_kwargs = {
    'name': 'aiges',
    'version': '0.4.3',
    'description': "A module for test aiges's python wrapper.py",
    'long_description': None,
    'author': 'maybaby',
    'author_email': 'ybyang7@iflytek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
