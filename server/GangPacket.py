#encoding = utf-8

class GangPacket(object):
    def __init__(self, op=None, data=None):
        self.__op = op or 0
        self.__data = data or b''
        self.__rpos = 0

    def WriteData(self, data):
        assert(isinstance(data,str))
        self.__data += data

    def ReadData(self, length):
        assert(self.__rpos+length<=len(self.__data))
        oldPos = self.__rpos
        self.__rpos += length
        return self.__data[oldPos:self.__rpos]

    def size(self):
        return len(self.__data)

    def opcode(self):
        return self.__op

    def data(self):
        return self.__data
