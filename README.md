# pcrjjc3

本插件是[pcrjjc2](https://github.com/cc004/pcrjjc2/tree/tw)的修改版

### 当然，pcrjjc3也有不带竞技场排名推送的版本，在[Lite分支](https://github.com/azmiao/pcrjjc3-tw/tree/lite)下

## 如何更新

一直摸兜里，直接`git pull`就完事了

## 重点注意

1. 本插件和pcrjjc2的绑定信息文件（即自动生成的`binds.json`）的数据结构稍有区别，无法通用。

    有相关动手能力的可以自己在原`binds.json`的每个人的绑定信息里增加一条来适配（例如下方就是指该玩家为1服）：
    ```
    "cx": "1"
    ```

2. 另外，和pcrjjc2一样，由于使用了不验证ssl的方式，因此可能产生ssl的验证warning [issue #7](https://github.com/azmiao/pcrjjc3-tw/issues/7)，可采用在hoshino文件夹下的`aiorequests.py`文件内加上几行：
    ```
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    ```
    来禁止该warning显示

3. 本插件现已支持每个群友自定义头像框，默认为彩色头像框（为[前川未来佬](https://github.com/shirakami-fubuki)从不知道什么鬼鬼地方使劲抠出来的彩框2333），其余rank框均为游戏解包抠出来的原图。

    如果你需要自己添加其他头像框也是没问题滴，直接把图片扔进本目录下的/img/frame/文件夹里即可，并且不用重启hoshinobot即可，大多数常见的图片格式一般都行，会自动转RGBA所以一般来说不用担心

4. 本插件现已支持自动更新版本号，妈妈再也不用担心我每次游戏版本更新时，都得手动改插件的版本号再重启hoshinobot了

## 命令

注意：数字3为服务器编号，支持1、2、3或4

关键词之间可以留空格也可以不留

| 关键词             | 说明                                                     |
| ------------------ | -------------------------------------------------------- |
| 竞技场绑定 3 uid   | 绑定竞技场排名变动推送，默认双场均启用，仅排名降低时推送 |
| 竞技场查询 3 uid   | 查询竞技场简要信息（绑定后无需输入3 uid）                |
| 停止竞技场订阅     | 停止战斗竞技场排名变动推送                               |
| 停止公主竞技场订阅 | 停止公主竞技场排名变动推送                               |
| 启用竞技场订阅     | 启用战斗竞技场排名变动推送                               |
| 启用公主竞技场订阅 | 启用公主竞技场排名变动推送                               |
| 竞技场历史         | 查询战斗竞技场变化记录（战斗竞技场订阅开启有效，可保留10条）|
| 公主竞技场历史     | 查询公主竞技场变化记录（公主竞技场订阅开启有效，可保留10条）|
| 删除竞技场订阅     | 删除竞技场排名变动推送绑定                               |
| 竞技场订阅状态     | 查看排名变动推送绑定状态                                 |
| 详细查询 3 uid     | 查询账号详细状态（绑定后无需输入3 uid）                  |
| 查询群数           | 查询bot所在群的数目                                      |
| 查询竞技场订阅数   | 查询绑定账号的总数量                                     |
| 查询头像框         | 查看自己设置的详细查询里的角色头像框                     |
| 更换头像框         | 更换详细查询生成的头像框，默认彩色                       |
| 清空竞技场订阅     | 清空所有绑定的账号(仅限主人)                             |

## 配置方法

1. 拿个不用的号登录PCR，然后把data/data/tw.sonet.princessconnect/shared_prefs/tw.sonet.princessconnect.v2.playerprefs.xml复制到该目录

    注意：每个服对应一个账号配置文件，并且每个号至少得开启加好友功能，四个服就要四份不同服的文件

2. 给你的tw.sonet.princessconnect.v2.playerprefs.xml加上前缀名，例如：
    ```
    台服一服：
    1cx_tw.sonet.princessconnect.v2.playerprefs.xml
    台服二服：
    2cx_tw.sonet.princessconnect.v2.playerprefs.xml
    台服三服：
    3cx_tw.sonet.princessconnect.v2.playerprefs.xml
    台服四服：
    4cx_tw.sonet.princessconnect.v2.playerprefs.xml
    ```
    如果没有某个服的配置文件或者不需要该服就不用管

3. 安装依赖：
    ```
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

4. 配置account.json设置代理：localhost就行，只要改端口，自行更换和你代理软件代理的端口一样就行，是代理端口哦，不是软件监听端口，开PAC模式不改变系统代理就行

    注意：如果你不需要代理，请打开`account.json`并将里面改成`{"proxy":{}}`

5. 开启插件，并重启Hoshino即可食用

## 更新日志

2022-03-27：新增自动更新插件内设置的游戏版本号

2022-03-27：新增竞技场历史记录查询

2022-03-24：新增自定义更换详细查询的头像框

2022-02-21：[详细查询整合为两张精美图片](https://github.com/azmiao/pcrjjc3-tw/pull/9)：新增个人资料卡界面图片生成与支援角色卡界面图片生成，并整合进详细查询中。

<details>
<summary>更以前的更新日志</summary>

2022-02-19：[优化并简化触发命令结构，可支持空格](https://github.com/azmiao/pcrjjc3-tw/commit/bc8413d944cdf4c17be62532494470878c9c9072)

2022-02-18：[更新README，并整合支援头像为一张图，](https://github.com/azmiao/pcrjjc3-tw/commit/98157067f590bb351c868c71bba3848b79afe80e)[close](https://github.com/azmiao/pcrjjc3-tw/commit/98157067f590bb351c868c71bba3848b79afe80e) [#7](https://github.com/azmiao/pcrjjc3-tw/issues/7)，[为了让时空祈梨能够完整显示日文名，调整了下位置，字体大小自适应以后再写吧2333](https://github.com/azmiao/pcrjjc3-tw/commit/3db3f161d835114247f12bc51ae2cdb08549be8c)

2022-02-16：[更详细的详细查询，支持查询支援角色](https://github.com/azmiao/pcrjjc3-tw/commit/c0eb4d969a5212db51c422b8155c94bbb0a6a823)，[查询信息中新增获取账号所在区服](https://github.com/azmiao/pcrjjc3-tw/commit/5f1e3d4a13f5b35bb7838221d1114a366f420ee9)，[修复KeyError: 'favorite_unit'报错](https://github.com/azmiao/pcrjjc3-tw/commit/d903a06c03f6d1aaf37ddf5ffcc7afad8157eaa3) 

2022-02-14：[update 2333](https://github.com/azmiao/pcrjjc3-tw/commit/59a780891926eddce225f984e4d2b578803cdd06)，[啊哈哈哈，寄汤来咯](https://github.com/azmiao/pcrjjc3-tw/commit/84568f9ff5db897fd14e509da77a7d2aa438ae08)，[为什么是requirement.txt而没有s，这不是复数吗](https://github.com/azmiao/pcrjjc3-tw/commit/ee4a79c844c23cf348db53e9d5d833f6b3f42797)

</details>

## 图片预览(来自电线佬的截图)
![4@{%Z%591B` YE1%}H0E7@1](https://user-images.githubusercontent.com/71607036/154960896-1d183705-0805-4f80-9cf2-6de13d35c5c3.jpg)

![FQ~} OTM$L20L6DAEI~RN`K](https://user-images.githubusercontent.com/71607036/154960912-6fd4f1fb-df38-4ef6-997c-af01b71810f4.PNG)

## 03-24 添加的自定义头像框后我的彩框截图

![寄！](https://cdn.jsdelivr.net/gh/azmiao/picture-bed/img/寄汤来咯.png)