# pcrjjc3-lite

本分支时pcrjjc3的精简版，删去了排名变动推送和排名变动历史，其他完全一致

## 为什么要有这个分支呢

比如说我就只想要查查排名就够了，毕竟是公会群，而且那个3分钟查一次后台日志看着有点难受（

但是呢，如果改动主分支爸推送放到一个新的service里面就可能影响之前使用的人，感觉不太好

## 如何更新

```
git pull origin lite
```

## 命令

注意：数字3为服务器编号，支持1、2、3或4

关键词之间可以留空格也可以不留

| 关键词             | 说明                                                     |
| ------------------ | -------------------------------------------------------- |
| 竞技场绑定 3 uid   | 绑定竞技场                                               |
| 竞技场查询 3 uid   | 查询竞技场简要信息（绑定后无需输入3 uid）                |
| 删除竞技场订阅     | 删除竞技场绑定                                          |
| 竞技场订阅状态     | 查看绑定状态                                             |
| 详细查询 3 uid     | 查询账号详细状态（绑定后无需输入3 uid）                  |
| 查询群数           | 查询bot所在群的数目                                      |
| 查询竞技场订阅数   | 查询绑定账号的总数量                                     |
| 查询头像框         | 查看自己设置的详细查询里的角色头像框                     |
| 更换头像框         | 更换详细查询生成的头像框，默认彩色                       |
| 清空竞技场订阅     | 清空所有绑定的账号(仅限主人)                             |