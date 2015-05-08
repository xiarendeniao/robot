#encoding=utf-8

import time, string
from pprint import pprint
from twisted.internet import task
from twisted.internet.protocol import ClientCreator
from twisted.internet import reactor
from Utils import *
from RobotProtocol import RobotProtocol

INIT                    = 1 #初始状态
CONNECTING_TO_GAME      = 2 #正在登陆游戏服
CONNECTED_TO_GAME       = 3 #正常连接状态

#自动重连时间
RECONNECT_SECONDS       = 30 #or None

class RobotMeta(type):
    def __new__(cls, name, bases, attrs):
        newbases = list(bases)
        import testcase
        import pkgutil
        for importer, modname, ispkg in pkgutil.iter_modules(testcase.__path__):
            if ispkg: continue
            mod = __import__('testcase.'+modname, globals(), locals(), fromlist=(modname,), level=1)
            if hasattr(mod, 'Robot'):
                newbases.append(mod.Robot)
        return super(RobotMeta, cls).__new__(cls, name, tuple(newbases), attrs)

class Robot():
    __metaclass__ = RobotMeta
    def __init__(self, name, passwd):
        #父类初始化函数
        clsObj = eval(self.__class__.__name__)
        for pclsObj in clsObj.__bases__:
            pclsObj.__init__(self)
        self.creator = ClientCreator(reactor, RobotProtocol)
        #属性赋值
        self.accountName = name
        self.passwd = passwd
        self.accountId = None
        self.charId = None
        self.charName = None
        self.status = INIT
        self.__ping_id = 0
        self.__last_pong = None
        self.__ping_task = None
        self.__check_pong_task = None
        self.x, self.z = 0, 0
        self.proto = None
        self.map = None
        self.testType = 'chat'
        self.mgr = None
        self.reconnectT = 0

        #定时执行的任务
        self.tasks = set()
        #推迟执行的任务
        self.delayedCalls = set()
        #检测上述两项合法性的任务
        self.checkTask = None
        
        def remove_old_data():
            #self.tasks在这里不好区分是否已经失效，所以应该由创建者管理(负责从这里删除)
            for tcall in list(self.delayedCalls):
                if not tcall.active():
                    self.delayedCalls.remove(tcall)
        self.checkTask = task.LoopingCall(remove_old_data)
        self.checkTask.start(10)
        
    def GenerateSeq(self):
        return 0

    def Connected(self, proto):
        self.proto = proto
        proto.robot = self
        if self.status == CONNECTING_TO_GAME:
            self.status = CONNECTED_TO_GAME
        else:
            assert(False)
        self.mgr.RobotConnected(self)
        
    def IsOnline(self):
        return self.status == CONNECTED_TO_GAME

    def DisConnected(self):
        #处理跟protocol的关系
        assert(self.proto)
        self.proto.robot = None
        del self.proto
        self.proto = None
        
        self.mgr.RobotDisconnected(self)
        self.__stop()
        
        #reconnect
        if self.reconnectT:
            log.msg('account(%s) to reconnect after %s seconds' % (self.accountName, self.reconnectT))
            reactor.callLater(self.reconnectT, self.ConnectToGameServer)
            self.reconnectT = 0
            return
        elif RECONNECT_SECONDS:
            log.msg('account(%s) to reconnect after %s seconds' % (self.accountName, RECONNECT_SECONDS))
            reactor.callLater(RECONNECT_SECONDS, self.ConnectToGameServer)
            return
        
    def DisConnect(self):
        if self.proto:
            log.msg('%s to close connection' % self.accountName)
            self.proto.transport.loseConnection()
        else:
            self.DisConnected()
        
    def TimedReconnect(self, seconds):
        log.msg('account(%s) to disconnect for timed reconnect' % (self.accountName, ))
        self.DisConnect()
        self.reconnectT = seconds
        
    def SendPacket(self, pkg):
        if self.proto:
            return self.proto.SendPacket(pkg)
        else:
            log.msg('account(%s) connection not found, drop packet %s' % (self.accountName, pkg.GetOpcode()))
                            
    def ConnectToGameServer(self):
        def cb(proto):
            log.msg('account(%s) connect to gameserver success' % (self.accountName, ))
            self.Connected(proto)
            self.Ping()
            self.StartTest()
        def err(e):
            log.msg('account(%s) connect to gameserver failed %r' % (self.accountName, e))
            self.status = INIT
            reactor.callLater(3, self. ConnectToGameServer)
        self.status = CONNECTING_TO_GAME
        self.creator.connectTCP(Config.HOST, Config.PORT).addCallbacks(cb, err)
    
    def Ping(self):
        def realping():
            pkg = GangPacket(PING)
            self.__ping_id += 1
            self.SendPacket(pkg)
        def checkpong():
            if not self.__ping_id: return
            if not self.__last_pong and self.__ping_id > 2:
                log.msg('%s none pong received' % (self.charName, ))
                self.DisConnect()
            if self.__last_pong and time.time() - self.__last_pong > 30:
                log.msg('%s none fresh pong received' % (self.charName, ))
                self.DisConnect()
        self.__ping_task = task.LoopingCall(realping)
        self.__ping_task.start(10)
        self.__check_pong_task = task.LoopingCall(checkpong)
        self.__check_pong_task.start(10)
        
    def PONG(self, pkg):
        self.__last_pong = time.time()
    
    def __stop(self):
        for t in self.delayedCalls:
            if t.active():
                t.cancel()
        self.delayedCalls.clear()
        
        for t in self.tasks:
            if t.running:
                t.stop()
        self.tasks.clear()
        
        if self.__ping_task and self.__ping_task.running:
            log.msg('account(%s) stop ping task' % self.accountName)
            self.__ping_task.stop()
        if self.__check_pong_task and self.__check_pong_task.running:
            log.msg('account(%s) stop check pong task' % self.accountName)
            self.__check_pong_task.stop()
        self.__ping_id = 0
        self.__last_pong = None
        self.__ping_task = None
        self.__check_pong_task = None
            
    def StartTest(self):
        testType = self.testType
        if testType:
            #执行参数指定的测试任务
            methodName = 'Test'+string.upper(testType[0])+string.lower(testType[1:])
            if hasattr(self, methodName):
                getattr(self, methodName)()
            else:
                log.msg('%s method "%s" not found' % (self.charName, methodName))
                assert(False)
        #随机断线和切换角色
        if Config.ROBUST_TEST:
            if random.randint(1,5) == 1:
                self.TimedReconnect(random.randint(0, 30))
            elif random.randint(1,5) == 1: 
                self.TimedReconnect(0) #断线马上重连，测试同账号多角色之间共享数据的问题
