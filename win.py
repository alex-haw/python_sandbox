import curses
from curses import ascii, panel, textpad
from loguru import logger
logger.add('pylog.log', level='DEBUG', mode='w')
from exctools import callif

class initscr:
    __exit__ = None

    def __new__(cls):
        return cls.__enter__(cls)
    
    def __enter__(self):
        self.__setattr__('__exit__', curses.wrapper)
        
        for atr in [atr for atr in self.__scr.__dir__() if atr.strip('_')==atr]:
            self.__setattr__(self, atr, self.__scr.__getattribute__(atr))

        return self