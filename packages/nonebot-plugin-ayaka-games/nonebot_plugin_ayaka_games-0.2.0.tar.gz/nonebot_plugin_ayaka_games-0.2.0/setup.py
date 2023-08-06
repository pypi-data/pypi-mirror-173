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
    'version': '0.2.0',
    'description': 'a pack of textual game on QQ via nonebot-plugin-ayaka',
    'long_description': '# ayaka文字小游戏合集 v0.2.0\n\n基于ayaka开发的文字小游戏合集（预计10个）\n\n任何问题请发issue\n\n<b>注意：由于更新pypi的readme.md需要占用版本号，因此其readme.md可能不是最新的，强烈建议读者前往[github仓库](https://github.com/bridgeL/nonebot-plugin-ayaka-games)以获取最新版本的帮助</b>\n\n# 快速了解\n\n## 基础功能\n1. 背包\n2. 签到\n\n## 游戏\n1. 印加宝藏 [@灯夜](https://github.com/lunexnocty/Meiri)\n2. 接龙（多题库可选，原神/成语）\n3. bingo\n4. 谁是卧底\n5. 抢30\n6. mana\n7. 加一秒\n\n# How to start\n\n## 安装 ayaka\n\n安装基础插件\n\nhttps://github.com/bridgeL/nonebot-plugin-ayaka\n\n## 安装 本插件\n\n安装本插件\n\n`poetry add nonebot-plugin-ayaka-games`\n\n修改nonebot2  `bot.py` \n\n```python\n# 导入ayaka_games插件\nnonebot.load_plugin("ayaka_games")\n```\n\n## 导入数据\n\n将本仓库的data文件夹，放到nonebot的工作目录下\n\n之后运行nonebot即可\n\n# 详细帮助\n\n启动bot后，可以使用help指令获取\n\n## 印加宝藏\n```\n   指令列表: \n   - incan 启动应用\n   - [start/run] 开始游戏\n   - [join] 加入游戏\n   - [status] 查看状态\n   - [go/back] 前进/撤退\n   - [rule/doc] 查看规则\n   - [exit/quit] 退出\n```\n## 接龙\n```\n  接龙，在聊天时静默运行\n\n  管理指令：\n  - 接龙 进入管理面板\n  - use <词库名称> 使用指定词库\n  - unuse <词库名称> 关闭指定词库\n  - list 列出所有词库\n  - data 展示你的答题数据\n  - rank 展示排行榜\n  - exit 退出管理面板\n```\n## bingo\n```\n  经典小游戏\n  - b <数字> 花费100金打开一张卡，当卡片练成一整行、一整列或一整条对角线时，获得200*n金的奖励\n  - bb <数字> 免费生成一张新的bingo表，默认大小为4\n```\n## 谁是卧底\n```\n  至少4人游玩，游玩前请加bot好友，否则无法通过私聊告知关键词\n\n  参与玩家的群名片不要重名，否则会产生非预期的错误=_=||\n\n  卧底只有一个\n  - 谁是卧底 打开应用\n  - help/帮助 查看帮助\n  - exit/退出 关闭应用\n\n  [room] 房间已建立，正在等待玩家加入...\n  - join/加入\n  - leave/离开\n  - start/begin/开始\n  - info/信息 展示房间信息\n  - exit/退出 关闭游戏\n    \n  [play] 游戏正在进行中...\n  - vote <at> 请at你要投票的对象，一旦投票无法更改\n  - info/信息 展示投票情况\n  - force_exit 强制关闭游戏，有急事可用\n```\n## 抢30\n```\n  至少2人游玩，一局内进行多轮叫牌，谁最先达到或超过30点谁获胜\n\n  总共52张牌，直到全部用完后才会洗牌，只要不退出游戏，下局的牌库将继承上局\n\n  首轮所有人筹码为10，每轮所有人筹码+1\n  - 抢30 打开应用\n  - help/帮助 查看帮助\n  - exit/退出 关闭应用\n    \n  [room] 房间已建立，正在等待玩家加入...\n  - join/加入\n  - leave/离开\n  - start/begin/开始\n  - info/信息 展示房间信息\n  - exit/退出 关闭游戏\n    \n  [play] 游戏正在进行中...\n  - 数字 报价叫牌，要么为0，要么比上一个人高，如果全员报价为0，则本轮庄家获得该牌\n  - info/信息 展示当前牌、所有人筹码、报价\n  - force_exit 强制关闭游戏，有急事可用\n```\n## mana\n```\n  ===== m a n a =====\n  欢愉、悼亡、深渊、智慧\n  ===== ======= =====\n\n  - 祈祷 <数字> 花费n玛娜，祈求神的回应\n  - 占卜 花费1玛娜，感受神的呼吸\n```\n\n## 加一秒\n\n```\n  每人初始时间值为0\n  每有3个不同的人执行一次或若干次加1，boss就会完成蓄力，吸取目前时间值最高的人的时间，如果有多人，则均吸取1点\n  boss时间值>=10时，游戏结束，时间值<=boss的人中，时间值最高的人获胜，一切重置\n  - 加一加 启动游戏\n  - exit/退出 退出游戏（数据保留）\n\n  游戏内指令：\n  - +1 让你的时间+1\n  - 我的 查看你目前的时间\n  - boss 查看boss的时间和能量\n  - 全部 查看所有人参与情况，以及boss的时间和能量\n```\n\n# 特别感谢\n\n[@灯夜](https://github.com/lunexnocty/Meiri) 大佬的插件蛮好玩的~\n\n',
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
