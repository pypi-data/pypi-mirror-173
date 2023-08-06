# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tortoise-stubs']

package_data = \
{'': ['*'], 'tortoise-stubs': ['fields/*']}

install_requires = \
['tortoise-orm']

setup_kwargs = {
    'name': 'types-tortoise',
    'version': '0.3.6',
    'description': 'Type stubs that make tortoise-orm a lot easier to work with when using type checkers.',
    'long_description': "# types-tortoise\n\n**Warning**: This package is deprecated. Use `tortoise-orm-stubs` instead.\n\nType stubs that make tortoise-orm a lot easier to work with when using type checkers.\n\nSpecifically,\n\n* ForeignKeyField can be typehinted without an extra type ignore\n* OneToOneField can be typehinted without an extra type ignore\n* Data fields' types are now automatically typehinted as the primitive types they describe, not Field subclasses\n* Data fields' types automatically reflect the value of null argument (i.e. become optional if you set null=True)\n",
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ovsyanka83/tortoise-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
