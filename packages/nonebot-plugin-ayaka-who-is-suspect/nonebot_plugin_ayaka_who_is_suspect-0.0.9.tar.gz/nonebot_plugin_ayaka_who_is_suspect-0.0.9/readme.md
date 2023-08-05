# 谁是卧底

基于ayaka开发的 谁是卧底 小游戏

任何问题请发issue

<b>注意：由于更新pypi的readme.md需要占用版本号，因此其readme.md可能不是最新的，强烈建议读者前往[github仓库](https://github.com/bridgeL/nonebot-plugin-ayaka-who-is-suspect)以获取最新版本的帮助</b>


# How to start

## 安装 ayaka

安装 [前置插件](https://github.com/bridgeL/nonebot-plugin-ayaka) 

`poetry add nonebot-plugin-ayaka`


## 安装 本插件

安装 本插件

`poetry add nonebot-plugin-ayaka-who-is-suspect`

修改nonebot2  `bot.py` 

```python
nonebot.load_plugin("ayaka_who_is_suspect")
```

## 导入数据

将本仓库的data文件夹（这是题库，可以自行修改，第一个是普通人，第二个是卧底词），放到nonebot的工作目录下

之后运行nonebot即可
