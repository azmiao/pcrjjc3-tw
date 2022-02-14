# pcrjjc3

本插件是[pcrjjc2](https://github.com/cc004/pcrjjc2/tree/tw)的修改版

新增了分服查询，但目前仍然不想支持一人绑定多号（总觉得会出问题）

## 重点注意

本插件和pcrjjc2的绑定信息文件（即自动生成的`binds.json`）的数据结构稍有区别，无法通用。

有相关动手能力的可以自己在原`binds.json`增加信息来适配（例如下方就是指该玩家为1服）：
```
"cx": "1"
```

## 命令

```
注意：下方uid格式样例：[3cx(原uid)]
(其中3为服务器编号，支持1或2或3或4)

[竞技场绑定 uid] 绑定竞技场排名变动推送，默认双场均启用，仅排名降低时推送
[竞技场查询 (uid)] 查询竞技场简要信息
[停止竞技场订阅] 停止战斗竞技场排名变动推送
[停止公主竞技场订阅] 停止公主竞技场排名变动推送
[启用竞技场订阅] 启用战斗竞技场排名变动推送
[启用公主竞技场订阅] 启用公主竞技场排名变动推送
[删除竞技场订阅] 删除竞技场排名变动推送绑定
[竞技场订阅状态] 查看排名变动推送绑定状态
[详细查询 (uid)] 查询账号详细状态
[查询群数] 查询bot所在群的数目
[查询竞技场订阅数] 查询绑定账号的总数量
[清空竞技场订阅] 清空所有绑定的账号(仅限主人)
```

## 支持版本

目前支持游戏版本：3.1.0

和之前的pcrjjc2一样，若后续游戏版本更新请自己打开`pcrclient.py`文件第18行
```
    'APP-VER' : '3.1.0',
```
修改游戏版本为当前最新，然后重启hoshinobot即可

## 配置方法

1. 拿个不用的号登录PCR，然后把data/data/tw.sonet.princessconnect/shared_prefs/tw.sonet.princessconnect.v2.playerprefs.xml复制到该目录

2. 给你的tw.sonet.princessconnect.v2.playerprefs.xml加上前缀名，例如：
    ```
    台服一服：
    1cx_tw.sonet.princessconnect.v2.playerprefs.xml
    台服二服：
    1cx_tw.sonet.princessconnect.v2.playerprefs.xml
    台服三服：
    1cx_tw.sonet.princessconnect.v2.playerprefs.xml
    台服四服：
    1cx_tw.sonet.princessconnect.v2.playerprefs.xml
    ```
    如果没有某个服的配置文件或者不需要该服就不用管

3. 安装依赖：
    ```
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

4. 配置account.json设置代理：localhost就行，只要改端口，自行更换和你代理软件代理的端口一样就行，是代理端口哦，不是软件监听端口，开PAC模式不改变系统代理就行

5. 开启插件，并重启Hoshino即可食用