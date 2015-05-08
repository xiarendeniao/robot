消息包长度      +   消息类型        +   验证信息        +   消息包
2bytes(大头)    +   2bytes(大头)    +   4bytes(小头)    +   ..

demo
    python main.py 10.6.20.184 5630 1,2,3-4 demo

获取角色列表、选取角色以后其他协议解析需要自行处理

这里只是展示了一个基本的流程

对于其他功能模块测试，可以仿照demo.py编写，testcase中的所有class Robot都会被框架自动整合到同一个Robot类上
