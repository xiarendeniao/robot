#encoding=utf-8

import random, math, time
from twisted.python import log
from GangPacket import GangPacket
from Opcodes import *

#config
class Config(object):
    ROBOT_SUFFIX_SET = set([1,2,3,4,5,6,7])
    SEQ_CHECK = True
    ROBUST_TEST = False #是否做健壮性测试，是则会随机的断线或强制跳出地图或者切换角色
    MULTI_CHAR = 4 #创建多个角色？0，否 非零，角色个数

def getTickCount():
    from datetime import datetime
    dt = datetime.now()
    return (dt.hour*3600 + dt.minute*60 + dt.second)*1000 + dt.microsecond/1000.0

def getRandDir():
    degrees = random.randint(0,360)
    return (math.cos(math.radians(degrees)), math.sin(math.radians(degrees)))

def calcDir(startX, startZ, endX, endZ):
    radians = math.atan2(endZ-startZ, endX-startX)
    cos = math.cos(radians)
    sin = math.sin(radians) 
    assert(0.99 < cos*cos+sin*sin < 1.01)
    return cos, sin

def calcDst(startX, startZ, endX, endZ):
    dx = endX - startX
    dz = endZ - startZ
    #rt2 = math.sqrt(dx*dx + dz*dz)
    return math.hypot(dx, dz)

import string
def str_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

