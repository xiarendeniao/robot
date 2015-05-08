#encoding=utf-8

import random
from Utils import *
from twisted.internet import task

class RobotMgr(object):
    
    def logfunc(self):
        print '************************************'
        print '* %s robots: %s online, %s offline' % (len(self.__robots), len(self.__online), len(self.__offline))
        print '************************************'
        
    def __init__(self):
        self.__robots = dict()
        self.__online = set()
        self.__offline = set()
        self.logTask = task.LoopingCall(self.logfunc)
        self.logTask.start(60)
        
    def AddRobot(self, robot):
        assert(robot.accountName not in self.__robots)
        self.__robots[robot.accountName] = robot
        self.__offline.add(robot)
        robot.mgr = self
        
    def DelRobot(self, robot):
        if robot.charName in self.__robots:
            del self.__robots[robot.accountName]
        robot.mgr = None
        if robot in self.__offline:
            self.__offline.remove(robot)
        if robot in self.__online:
            self.__online.remove(robot)

    def RobotConnected(self, robot):
        assert(robot.accountName in self.__robots)
        if robot in self.__offline:
            self.__offline.remove(robot)
        self.__online.add(robot)
        self.logfunc()

    def RobotDisconnected(self, robot):
        assert(robot.accountName in self.__robots)
        if robot in self.__online: 
            self.__online.remove(robot)
        self.__offline.add(robot)
        self.logfunc()
        
    def GetRandomRobot(self):
        if len(self.__online) == 0:
            return None
        else:
            accountName = random.choice(self.__robots.keys()) 
            target = self.__robots[accountName]
            if target.IsOnline():
                return target
            else:
                return None
