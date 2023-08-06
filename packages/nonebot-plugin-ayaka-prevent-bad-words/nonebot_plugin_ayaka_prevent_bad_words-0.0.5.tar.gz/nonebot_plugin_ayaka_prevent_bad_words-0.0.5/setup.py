# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['ayaka_prevent_bad_words']
install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-ayaka>=0.3.10,<0.4.0',
 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-prevent-bad-words',
    'version': '0.0.5',
    'description': '坏词撤回',
    'long_description': '# 坏词撤回\n\n基于[ayaka](https://github.com/bridgeL/nonebot-plugin-ayaka)开发的 坏词撤回 插件\n\n任何问题请发issue\n\n- 自动撤回包含屏蔽词的消息\n- 只适用于群聊\n- 管理员无法撤回其他管理员和群主的发言\n\n<b>注意：由于更新pypi的readme.md需要占用版本号，因此其readme.md可能不是最新的，强烈建议读者前往[github仓库](https://github.com/bridgeL/nonebot-plugin-ayaka-prevent-bad-words)以获取最新版本的帮助</b>\n\n\n# How to start\n\n## 安装插件\n\n`poetry add nonebot-plugin-ayaka-prevent-bad-words`\n\n## 导入插件\n\n修改nonebot2  `bot.py` \n\n```python\nnonebot.load_plugin("ayaka_prevent_bad_words")\n```\n\n## 修改屏蔽词列表\n文件位置：`data/plugins/坏词撤回/words.txt`（该文件在第一次启动时会自动生成）\n\n一行一个敏感词\n\n```\n芝士雪豹\n雪豹闭嘴\n```\n\n之后群友发言包含这些词时会被撤回\n\n\n## 其他配置\n文件位置：`data/plugins/坏词撤回/config.json`（该文件在第一次启动时会自动生成）\n\n`delay` \n\n延迟n秒后撤回，默认为0\n\n可能会因为网络延迟而不准确\n\n`powerful` \n\n检测力度，默认为0\n\n| powerful | 效果                               |\n| -------- | ---------------------------------- |\n| -1       | 发出提示语，不撤回                 |\n| 0        | 只有坏词完全匹配时，才会撤回       |\n| 1        | 即使坏词中夹杂了标点符号，也会撤回 |\n\n`tip` \n\n提示语，默认为 请谨言慎行\n\n**注意：修改配置后，需要重启bot才能生效**\n\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-prevent-bad-words',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
