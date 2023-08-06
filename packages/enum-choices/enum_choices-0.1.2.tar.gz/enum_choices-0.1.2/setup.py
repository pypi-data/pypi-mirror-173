# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enum_choices']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enum-choices',
    'version': '0.1.2',
    'description': 'a choices',
    'long_description': 'None',
    'author': 'huoyinghui',
    'author_email': 'yhhuo@yunjinginc.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pydtools/choices/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
