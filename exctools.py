from loguru import logger
from functools import wraps

def _noop(*_, **__): return None

def callif(condition = lambda _: True,
           truecall = _noop,
           falsecall = _noop,
           exccall = _noop,
           passexc = (),
           logexc = (Exception,),
           reraisexc = (BaseException,),
           args = (),
           kwargs = {}):
    for cb in truecall, falsecall, exccall:
        if cb == None: cb = _noop
    
    @logger.catch(exception=reraisexc, exclude=(*logexc, *reraisexc), reraise=True,
                  onerror=_noop, level='ERROR')
    @logger.catch(exclude=passexc, exception=logexc, reraise=False,
                  onerror= lambda _: exccall(*args, **kwargs), level='WARNING')
    @logger.catch(exclude=logexc, exception=passexc, reraise=False,
                  onerror= lambda _: exccall(*args, **kwargs), level='TRACE')
    def exception_cascade():
        nonlocal condition, truecall, falsecall, args, kwargs
        try:
            if callable(condition): condition = condition()
        except (*logexc, *reraisexc) as conE:
            condition = False
        finally:
            return (truecall if condition else falsecall)(*args, **kwargs)
    return(exception_cascade())
