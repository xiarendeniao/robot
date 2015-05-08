#encoding=utf-8
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from GangPacket import *
import logging, struct

#包头长度
HEADER_LEN = 2
#命令长度
OPCODE_LEN = 2
#验证信息长度
VERF_LEN = 4

class ConsoleFactory(Factory):
    '''
       listen console connect & accept console command. 
    '''
    class MyProtocol(Protocol):
        def __init__(self, factory):
            self.factory = factory
            self.__pkg_size = None
            self.__pkg_data = b''
    
        def connectionMade(self):
            logging.info("console client connected")
    
        def connectionLost(self, reason):
            logging.info("console client closed")
    
        def dataReceived(self, data):
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
                if opcode == 1:
                    logging.info('recv PING')
                    rpkg = GangPacket(2)
                    self.SendPacket(rpkg)
                    logging.info('sent PONG')
                elif opcode == 3:
                    num = struct.unpack('>H', t.ReadData(2))[0]
                    logging.info('recv C_TEST: %d' % num)
                    rpkg = GangPacket(4)
                    num += 1
                    rpkg.WriteData(struct.pack('>H', num))
                    self.SendPacket(rpkg)
                    logging.info('sent G_TEST: %d' % num)
                else:
                    assert(false)
                #重置数据接收区域
                self.__pkg_data = self.__pkg_data[self.__pkg_size:]
                self.__pkg_size = None         
    
        def SendPacket(self, pkg):
            fulldata = struct.pack('>H', pkg.size()+OPCODE_LEN+VERF_LEN) + struct.pack('>H', pkg.opcode()) + struct.pack('<I',0) + pkg.data()
            self.transport.write(fulldata)

    def buildProtocol(self, addr):
        return self.MyProtocol(self)

def start(port):
    '''
    listen console port
    '''
    logging.info("listening %d for console.." % port)
    reactor.listenTCP(port, ConsoleFactory())
    reactor.run()
