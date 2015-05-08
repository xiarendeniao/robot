#encoding=utf-8

import struct
from twisted.internet.protocol import Protocol
from Utils import *
from Opcodes import *

#是否输出收发包日志
PKG_LOG = True

#包头长度
HEADER_LEN = 2
#命令长度
OPCODE_LEN = 2
#验证信息长度
VERF_LEN = 4

class RobotProtocol(Protocol):    
    def __init__(self):
        self.__pkg_size = None
        self.__pkg_data = b''
        self.__connected = False
        self.robot = None
        
    def GetRobotName(self):
        if self.robot:
            if self.robot.charName:
                logName = self.robot.charName+' '
            else: 
                logName = 'account(%s) ' % self.robot.accountName
        else: logName = ''
        return logName
        
    def dataReceived(self, data):
        self.__readdata(data)
        
    def connectionLost(self, reason):
        log.msg('%sconnection losted: %r' % (self.GetRobotName(), reason))
        self.__connected = False
        if self.robot:
            self.robot.DisConnected()
        
    def connectionMade(self):
        log.msg('%sconnection made' % self.GetRobotName())
        self.__connected = True
        
    def SendPacket(self, pkg):
        seq = self.robot.GenerateSeq()
        fulldata = struct.pack('>H', pkg.size()+OPCODE_LEN+VERF_LEN) + struct.pack('>H', pkg.opcode()) + struct.pack('<I',seq) + pkg.data()

        if self.__senddata(fulldata):
            if PKG_LOG:
                log.msg('%ssent %s(0x%03X) %d bytes' % (self.GetRobotName(), opcodes[pkg.opcode()], pkg.opcode(), pkg.size()))
            
    def IsConnected(self):
        return self.__connected
        
    def __senddata(self, data):
        if not self.__connected:
            log.msg('%sconnection not found' % self.GetRobotName())
            return False
        else:
            rt = self.transport.write(data)
            return True
        
    def __readdata(self, data):
        self.__pkg_data += data
        while True:
            if self.__pkg_size == None:
                #解析网络包长度
                if len(self.__pkg_data) >= HEADER_LEN:
                    self.__pkg_size = struct.unpack('>H', self.__pkg_data[0:HEADER_LEN])[0]
                    assert(self.__pkg_size >= OPCODE_LEN + VERF_LEN)
                    self.__pkg_data = self.__pkg_data[HEADER_LEN:]
                else:
                    return
            #等待更多的数据
            if len(self.__pkg_data) < self.__pkg_size:
                return
            #解析命令
            opcode = struct.unpack('>H', self.__pkg_data[0:OPCODE_LEN])[0]
            t = GangPacket(opcode, self.__pkg_data[OPCODE_LEN+VERF_LEN:self.__pkg_size])
            #执行对应的处理函数
            if opcode not in opcodes:
                if PKG_LOG:
                    log.msg('%sunrecognized 0x%03X %d bytes.' % (self.GetRobotName(), opcode, self.__pkg_size-OPCODE_LEN))
            else:
                opcodeStr = opcodes[opcode]
                if not hasattr(self.robot, opcodeStr):
                    if PKG_LOG:
                        log.msg('%signored %s(0x%03X) %d bytes' % (self.GetRobotName(), opcodeStr, opcode, self.__pkg_size-OPCODE_LEN))
                else:
                    if PKG_LOG:
                        log.msg('%sreceived %s(0x%03X) %d bytes' % (self.GetRobotName(), opcodeStr, opcode, self.__pkg_size-OPCODE_LEN))
                    getattr(self.robot, opcodeStr)(GangPacket(opcode, self.__pkg_data[OPCODE_LEN+VERF_LEN:self.__pkg_size]))
            #重置数据接收区域
            self.__pkg_data = self.__pkg_data[self.__pkg_size:]
            self.__pkg_size = None
