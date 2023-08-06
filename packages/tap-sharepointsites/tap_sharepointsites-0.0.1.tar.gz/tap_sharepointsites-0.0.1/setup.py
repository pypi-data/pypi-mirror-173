# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_sharepointsites',
 'tap_sharepointsites.tests',
 'tap_sharepointsites.tests.configuration']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity>=1.11,<2.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['tap-sharepointsites = '
                     'tap_sharepointsites.tap:Tapsharepointsites.cli']}

setup_kwargs = {
    'name': 'tap-sharepointsites',
    'version': '0.0.1',
    'description': '`tap-sharepointsites` is a Singer tap for sharepointsites, built with the Meltano Singer SDK.',
    'long_description': 'None',
    'author': 'Henning Holgersen',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
