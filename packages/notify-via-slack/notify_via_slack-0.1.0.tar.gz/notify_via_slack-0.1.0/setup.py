# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack']

package_data = \
{'': ['*']}

install_requires = \
['python-decouple>=3.6,<4.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'slack-sdk>=3.19.2,<4.0.0']

setup_kwargs = {
    'name': 'notify-via-slack',
    'version': '0.1.0',
    'description': 'notify messages on channels',
    'long_description': '',
    'author': 'Lucas',
    'author_email': 'lucassrod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lucassimon/slack-notifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
