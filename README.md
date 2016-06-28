# robot
/robot是机器人客户端代码
/server接受robot的连接和数据、并给予简单的反馈，仅仅是用于演示robot程序而已
这是写出来给另一个公司的同学用的，所以足够简洁和业务逻辑无关

我在自己工作的项目中写的机器人比这个好用:
  用C++扩展了封包拆包、加密、地图解析、寻路等逻辑
  提供了一些数据转换、模拟GMT的工具
  
因使用技术跟公司技术方向不符而不太受重视，不过个人感觉机器人对于服务端的稳定性测试、压力测试、逻辑测试（主要是多人PVP、GVG）、分线控制还是提供了很有力的辅助的。等以后对项目没影响以后再把代码放到github上来。

[root@test-22 kl-robot]# python main.py -h
usage: main.py [-h] [-H HOST] [-P PORT]
               [-t {all,chat,move,arena,duobao,arenapvp,yingling,shengjian,xieshen,guild,room,gvg,attack,skill,solo,equip,dragon,heroseat}]
               [-s SUFFIX] [-a ACCOUNTNAME] [--passWord PASSWORD]
               [--version VERSION] [-c CHARNAME] [--tollId TOLLID]
               [--multi-char MULTICHAR] [--no-market] [--no-robust]
               [-p ACCOUNT_PREFIX] [--verbose-log]
               [--account-file ACCOUNTFILE] [--server-name SERVERNAME]
               [--encrypt-seed ENCRYPTSEED] [--no-encrypt]

*************kl robot**************

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  服务器IP
  -P PORT, --port PORT  服务器端口
  -t {all,chat,move,arena,duobao,arenapvp,yingling,shengjian,xieshen,guild,room,gvg,attack,skill,solo,equip,dragon,heroseat}, --testcase {all,chat,move,arena,duobao,arenapvp,yingling,shengjian,xieshen,guild,room,gvg,attack,skill,solo,equip,dragon,heroseat}
                        要测试的功能模块
  -s SUFFIX, --suffix SUFFIX
                        机器人的后缀，用于控制机器人数量，可
                        用","分隔数字、用"-"表示范围
  -a ACCOUNTNAME, --accountName ACCOUNTNAME
                        指定账号登陆,设置该参数则suffix失效
  --passWord PASSWORD   指定密码登陆
  --version VERSION     制定版本号
  
  -c CHARNAME, --charName CHARNAME
                        指定角色登陆
  --tollId TOLLID       关卡ID
  --multi-char MULTICHAR
                        为每个账号创建指定数量的角色
  --no-market           取消商城和领奖的测试: 随机消费和领奖
  --no-robust           取消健壮型测试:
                        随机断线、重连、切换角色
  -p ACCOUNT_PREFIX, --prefix ACCOUNT_PREFIX
                        账号前缀
  --verbose-log         详细日志
  --account-file ACCOUNTFILE
                        批量指定账号密码登陆,设置该参数则suffi
                        x/prefix/accountName/charName都失效
  --server-name SERVERNAME
                        指定游戏服名字
  --encrypt-seed ENCRYPTSEED
                        加密seed
  --no-encrypt          取消加密
