# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gurobipy_helper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gurobipy-helper',
    'version': '0.0.1a10',
    'description': 'A library adding some functionality to the Gurobi library.',
    'long_description': '# gurobipy_helper\n\nA library which adds what I need.',
    'author': 'Nico Strasdat',
    'author_email': 'nstrasdat@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wotzlaff/gurobipy_helper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}
from build_lib import *
build(setup_kwargs)

setup(**setup_kwargs)
