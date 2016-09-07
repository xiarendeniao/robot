robot

    客户端
    
    在实际应用中可以加上加密、地图解析、寻路等逻辑，用于服务端的稳定性测试、压力测试、逻辑测试（主要是多人PVP、GVG）、分线控制等

    demo只是展示了一个基本的流程,对于其他功能模块测试，可以仿照demo.py编写

    testcase中的所有class Robot都会被框架自动整合到同一个Robot类上

    python main.py serverIP serverPort 1,2,3-4 demo #启动4个robot(robot1/robot2/robot3/robot4)连接服务器做demo模块测试

server

    服务器,用于演示robot程序
    
    接受robot连接、对于robot发来的数据并给予简单的反馈
    
    PING -> PONG

    C_TEST -> G_TEST

    python main.py #默认listen 8765端口

协议(tcp)

    消息包长度      +   消息类型        +   验证信息        +   消息包
    2bytes(大头)    +   2bytes(大头)    +   4bytes(小头)    +   ..
