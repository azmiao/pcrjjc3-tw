# pcrjjc3

本插件是[pcrjjc2](https://github.com/cc004/pcrjjc2/tree/tw)的修改版

新增了分服查询和分服绑定

## 注意

本插件和pcrjjc2的绑定信息文件（即自动生成的`binds.json`）的数据结构稍有区别，无法通用。

有相关动手能力的可以自己在原`binds.json`增加信息来适配（例如下方就是指该玩家为1服）：
```
"cx": "1"
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