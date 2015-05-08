#encoding=utf-8
import logging
import Console

#log config
g_logLevel = logging.DEBUG  
g_logFormat = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]%(message)s"  

if __name__ == "__main__":
    logging.basicConfig(level=g_logLevel,format=g_logFormat,stream=None)
    Console.start(8765)
