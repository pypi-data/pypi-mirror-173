# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['container_collection',
 'container_collection.docker',
 'container_collection.jobs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.0,<2.0.0', 'prefect>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'container-collection',
    'version': '0.1.0',
    'description': 'Collection of tasks for running containerized models.',
    'long_description': '[![Build Status](https://github.com/bagherilab/container-collection/workflows/build/badge.svg)](https://github.com/bagherilab/container-collection/actions?query=workflow%3Abuild)\n[![Codecov](https://img.shields.io/codecov/c/gh/bagherilab/container-collection?token=OH8080ZFCU)](https://codecov.io/gh/bagherilab/container-collection)\n[![Lint Status](https://github.com/bagherilab/container-collection/workflows/lint/badge.svg)](https://github.com/bagherilab/container-collection/actions?query=workflow%3Alint)\n[![Documentation](https://github.com/bagherilab/container-collection/workflows/documentation/badge.svg)](https://bagherilab.github.io/container-collection/)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n',
    'author': 'Jessica S. Yu',
    'author_email': 'jesyu@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
