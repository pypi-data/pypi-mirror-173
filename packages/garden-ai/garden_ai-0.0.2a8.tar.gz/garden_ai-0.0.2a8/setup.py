# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['garden_ai']

package_data = \
{'': ['*']}

install_requires = \
['globus-sdk>=3.12.0,<4.0.0', 'requests>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'garden-ai',
    'version': '0.0.2a8',
    'description': 'Garden: tools to simplify access to scientific AI advances.',
    'long_description': '# Garden\n\n[![NSF-2209892](https://img.shields.io/badge/NSF-2209892-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2209892&HistoricalAwards=false)\n[![PyPI](https://badge.fury.io/py/garden-ai.svg)](https://badge.fury.io/py/garden-ai)\n[![Tests](https://github.com/Garden-AI/garden/actions/workflows/pypi.yaml/badge.svg)](https://github.com/Garden-AI/garden/actions/workflows/pypi.yaml)\n[![tests](https://github.com/Garden-AI/garden/actions/workflows/ci.yaml/badge.svg)](https://github.com/Garden-AI/garden/actions/workflows/ci.yaml)\n\n\n## Support\nThis work was supported by the National Science Foundation under NSF Award Number: 2209892 "Frameworks: Garden: A FAIR Framework for Publishing and Applying AI Models for Translational Research in Science, Engineering, Education, and Industry".\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
