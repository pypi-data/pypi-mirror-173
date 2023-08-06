# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basedtyping']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'basedtyping',
    'version': '0.0.2',
    'description': 'Utilities for basedmypy',
    'long_description': 'None',
    'author': 'DetachHead',
    'author_email': 'detachhead@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
