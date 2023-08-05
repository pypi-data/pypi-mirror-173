# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdc_logger']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-logging', 'nisa-di', 'pydantic']

setup_kwargs = {
    'name': 'pdc-logger',
    'version': '1.0.4',
    'description': 'standarized python logger pdc',
    'long_description': '# Pdc_logger\ngcloud centralized logging for pdc\n\n\n\n# Setup credential google\n\nset GOOGLE_APPLICATION_CREDENTIALS=credentials.json\n\n\n\n# Cara Pakai\n\nTanya Programmer PDC sama Bawa gorengan',
    'author': 'vaziria',
    'author_email': 'manorder123@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
