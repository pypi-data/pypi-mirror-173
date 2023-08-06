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
    'version': '0.1.1',
    'description': 'notify messages on channels',
    'long_description': "# Notify via slack\n\nInstall: `pip install notify-via-slack`\n\n## Usage\n\nCreate an app in [slack api](https://api.slack.com/apps)\n\nSave the bot token\n\nCopy the .env.example to .env `cp .env.example .env`\n\nReplace the `SLACK_BOT_TOKEN`\n\nSend a message\n\n```python\nslack.notify import SlackNotify\n\nhandler = SlackNotify(app_name='My app name')\nhandler.notify(message='some message', emit_log=True, is_error=True)\n\n```\n",
    'author': 'Lucas',
    'author_email': 'lucassrod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lucassimon/notify-via-slack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
