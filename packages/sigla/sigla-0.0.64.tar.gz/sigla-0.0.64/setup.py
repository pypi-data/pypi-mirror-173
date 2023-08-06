# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigla',
 'sigla.cli',
 'sigla.data',
 'sigla.frontmatter',
 'sigla.nodes',
 'sigla.templates',
 'sigla.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2==3',
 'black==22.10.0',
 'configparser>=5.0.1,<6.0.0',
 'environ-config>=20.1.0,<21.0.0',
 'flake8-cognitive-complexity>=0.1.0,<0.2.0',
 'inquirer>=2.7.0,<3.0.0',
 'mypy==0.982',
 'pretty-errors>=1.2.19,<2.0.0',
 'pydash>=4.9.1,<5.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer==0.6.1']

entry_points = \
{'console_scripts': ['sigla = sigla.cli.cli:app']}

setup_kwargs = {
    'name': 'sigla',
    'version': '0.0.64',
    'description': 'Yet another code generator',
    'long_description': 'None',
    'author': 'mg santos',
    'author_email': 'mauro.goncalo@gmail.com',
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
