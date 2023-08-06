# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka_games', 'ayaka_games.user_bag']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-ayaka>=0.3.8,<0.4.0',
 'nonebot2>=2.0.0b5,<3.0.0',
 'pypinyin>=0.47.1,<0.48.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-games',
    'version': '0.2.1',
    'description': 'a pack of textual game on QQ via nonebot-plugin-ayaka',
    'long_description': '<div align="center">\n\n# ayaka文字小游戏合集 v0.2.1\n\n基于ayaka开发的文字小游戏合集（预计10个）\n\n[仓库](https://github.com/bridgeL/nonebot-plugin-ayaka-games) - \n[文档](https://bridgel.github.io/ayaka_doc/games/)\n\n</div>\n\n任何问题欢迎issue\n\n## 基础功能\n1. 背包\n2. 签到\n\n## 游戏\n1. 印加宝藏 [@灯夜](https://github.com/lunexnocty/Meiri)\n2. 接龙（多题库可选，原神/成语）\n3. bingo\n4. 谁是卧底\n5. 抢30\n6. mana\n7. 加一秒\n\n## 安装 \n\n1. 安装 ayaka https://github.com/bridgeL/nonebot-plugin-ayaka\n2. 安装 本插件 `poetry add nonebot-plugin-ayaka-games`\n3. 修改nonebot2  `bot.py` \n\n```python\n# 导入ayaka_games插件\nnonebot.load_plugin("ayaka_games")\n```\n\n4. 导入数据\n\n将本仓库的data文件夹，放到nonebot的工作目录下\n\n之后运行nonebot即可\n\n\n# 特别感谢\n\n[@灯夜](https://github.com/lunexnocty/Meiri) 大佬的插件蛮好玩的~\n\n\n# 文档\n\nhttps://bridgel.github.io/ayaka_doc/games/\n\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-games',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
