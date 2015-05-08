#encoding=utf-8

import sys
from twisted.internet import reactor
from src.Utils import *
from src.Robot import Robot
from src.RobotMgr import RobotMgr
from twisted.python import log, util

def myFLOemit(self,eventDict):
    """Custom emit for FileLogObserver"""
    text = log.textFromEventDict(eventDict)
    if text is None:
        return
    self.timeFormat='[%Y-%m-%d %H:%M:%S]'
    timeStr = self.formatTime(eventDict['time'])
    fmtDict = {'text': text.replace("\n", "\n\t")}
    msgStr = log._safeFormat("%(text)s\n", fmtDict)
    util.untilConcludes(self.write, timeStr + " " + msgStr)
    util.untilConcludes(self.flush)

def main(testType):
    log.FileLogObserver.emit = myFLOemit
    log.startLogging(sys.stdout)
    robotMgr = RobotMgr()
    for i in Config.ROBOT_SUFFIX_SET:
        robot = Robot('robot'+str(i), '1')
        robot.testType = testType
        robotMgr.AddRobot(robot)
        robot.ConnectToGameServer()
    reactor.run()

if __name__ == '__main__':
    testType = 'move'
    if len(sys.argv) > 1:
        Config.HOST = sys.argv[1].strip()
    if len(sys.argv) > 2:
        Config.PORT = int(sys.argv[2].strip())
    if len(sys.argv) > 3:
        tmpStr = sys.argv[3]
        strList = tmpStr.strip().split(',')
        suffixSet = set()
        for t in strList:
            tmpList = t.strip().split('-')
            if len(tmpList)==2 and tmpList[0].isdigit() and tmpList[1].isdigit() and int(tmpList[0])<=int(tmpList[1]):
                suffixSet |= set(range(int(tmpList[0]),int(tmpList[1])+1))
            else:
                suffixSet.add(t.strip())
        Config.ROBOT_SUFFIX_SET = suffixSet                 
            
    if len(sys.argv) > 4:
        testType = sys.argv[4].strip()
    else:
        testType = ''
    main(testType)
