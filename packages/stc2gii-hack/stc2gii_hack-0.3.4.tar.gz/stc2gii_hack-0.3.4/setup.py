# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stc2gii_hack']

package_data = \
{'': ['*']}

install_requires = \
['mne==1.0.2', 'nibabel>=3.2.2,<4.0.0', 'numpy>=1.22.3,<2.0.0']

entry_points = \
{'console_scripts': ['stc2gii_hack = stc2gii_hack.run_hack:main']}

setup_kwargs = {
    'name': 'stc2gii-hack',
    'version': '0.3.4',
    'description': '',
    'long_description': None,
    'author': 'Joshua Teves',
    'author_email': 'joshua.teves@nih.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
