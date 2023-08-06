# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-rc.1,<3.0.0', 'sqlalchemy[asyncio]>=1.4.42,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-sqlalchemy',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
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
