# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niaaml_gui',
 'niaaml_gui.widgets',
 'niaaml_gui.windows',
 'niaaml_gui.windows.threads']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.0,<6.0.0',
 'QtAwesome>=1.0.2,<2.0.0',
 'niaaml>=1.1.11,<2.0.0',
 'niapy>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['NiaAML-GUI = niaaml_gui.main:run']}

setup_kwargs = {
    'name': 'niaaml-gui',
    'version': '0.1.13',
    'description': 'GUI for NiaAML Python package',
    'long_description': '',
    'author': 'Luka Pečnik',
    'author_email': 'lukapecnik96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukapecnik/NiaAML-GUI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
