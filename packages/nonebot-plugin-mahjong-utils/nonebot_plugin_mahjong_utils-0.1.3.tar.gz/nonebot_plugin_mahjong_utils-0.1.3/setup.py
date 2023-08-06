# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_mahjong_utils',
 'nonebot_plugin_mahjong_utils.interceptors',
 'nonebot_plugin_mahjong_utils.matchers',
 'nonebot_plugin_mahjong_utils.utils']

package_data = \
{'': ['*']}

install_requires = \
['mahjong-utils>=0.1.0a4,<0.2.0', 'nonebot2>=2.0.0rc1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mahjong-utils',
    'version': '0.1.3',
    'description': '',
    'long_description': 'nonebot-plugin-mahjong-utils\n========',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ssttkkl/nonebot-plugin-mahjong-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
