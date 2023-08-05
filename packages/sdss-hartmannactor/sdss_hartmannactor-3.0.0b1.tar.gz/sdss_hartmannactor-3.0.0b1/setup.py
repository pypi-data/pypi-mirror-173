# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['hartmann', 'hartmann.actor']

package_data = \
{'': ['*'], 'hartmann': ['etc/*']}

install_requires = \
['astropy>=5.0,<6.0',
 'click-default-group>=1.2.2,<2.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'scipy>=1.8.0,<2.0.0',
 'sdss-clu>=1.6.2,<2.0.0',
 'sdsstools>=0.5.0',
 'seaborn>=0.11.2,<0.12.0']

entry_points = \
{'console_scripts': ['hartmann = hartmann.__main__:hartmann']}

setup_kwargs = {
    'name': 'sdss-hartmannactor',
    'version': '3.0.0b1',
    'description': 'An actor to analyse hartmann images and apply corrections.',
    'long_description': '# hartmannActor\n\n![Versions](https://img.shields.io/badge/python->=3.9-blue)\n[![Test](https://github.com/sdss/hartmannActor/actions/workflows/test.yml/badge.svg)](https://github.com/sdss/hartmannActor/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/sdss/hartmannActor/branch/py3/graph/badge.svg)](https://codecov.io/gh/sdss/hartmannActor)\n\nThis commands the BOSS ICC or yao to take Hartmann exposures, calculates the focus of the exposures, and if needed informs BOSS ICC / yao to apply focus corrections to the collimator, and also the blue ring.\n',
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sdss/hartmannActor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
