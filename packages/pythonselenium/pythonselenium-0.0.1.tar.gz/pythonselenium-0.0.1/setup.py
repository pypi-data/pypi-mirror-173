# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pythonselenium']
setup_kwargs = {
    'name': 'pythonselenium',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'coderstack',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
