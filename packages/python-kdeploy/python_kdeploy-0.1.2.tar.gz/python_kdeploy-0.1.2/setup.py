# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_kdeploy', 'python_kdeploy.invoke_generator']

package_data = \
{'': ['*']}

install_requires = \
['invoke>=1.7.3,<2.0.0',
 'patchwork>=1.0.1,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'types-toml>=0.10.8,<0.11.0']

entry_points = \
{'console_scripts': ['pydep = python_kdeploy.entry:cmd']}

setup_kwargs = {
    'name': 'python-kdeploy',
    'version': '0.1.2',
    'description': 'simple package for deployment on remote machine',
    'long_description': '# python-deploy\n\nProject for python application deployment into service.\n\n\n## Basics\n1. check command `pydep -h` for help.\n2. configure `config.toml` file.\n3. put your docker files into same dir.\n',
    'author': 'Ilya Kaftanov',
    'author_email': 'kaftanovwork@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/IKaftanov/python-deploy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
