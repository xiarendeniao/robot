#encoding=utf-8

import string
from twisted.internet import reactor
from twisted.internet import task
from pprint import pprint
from ..Utils import *
from ..Opcodes import *
import struct

class Robot(object):
    def __init__(self):
        pass
        
    def G_TEST(self, pkg):
        rt, = struct.unpack('>H', pkg.ReadData(2))
        log.msg('%s recv G_TEST: %d' % (self.accountName, rt))
        
    def TestDemo(self):
        def realDemo():
            pkg = GangPacket(C_TEST)
            num = random.randint(1,200)
            log.msg('%s sent C_TEST: %d' % (self.accountName, num))
            pkg.WriteData(struct.pack('>H', num))
            self.SendPacket(pkg)
        ttask = task.LoopingCall(realDemo)
        ttask.start(2)
        self.tasks.add(ttask)
