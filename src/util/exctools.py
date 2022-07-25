from loguru import logger
from functools import wraps

def _noop(*_, **__): return None

def callif(condition = lambda _: True,
           true_call = _noop, false_call = _noop, exc_call = _noop,
           pass_exc = (), warn_exc = (Exception,), raise_exc = (BaseException,),
           args = (), kwargs = {}):
    """
    Conditionally call a function and handle exceptions selectively

    """
    for cb in true_call, false_call, exc_call:
        if cb == None: cb = _noop
    
    @logger.catch(exception=raise_exc, exclude=(*warn_exc, *raise_exc), reraise=True,
                  onerror=_noop, level='ERROR')
    @logger.catch(exception=warn_exc, exclude=pass_exc, reraise=False,
                  onerror= lambda _: exc_call(*args, **kwargs), level='WARNING')
    @logger.catch(exception=pass_exc, exclude=warn_exc, reraise=False,
                  onerror= lambda _: exc_call(*args, **kwargs), level='TRACE')
    def exception_cascade():
        nonlocal condition, true_call, false_call, args, kwargs
        try:condition = condition() if callable(condition) else condition
        except (*warn_exc, *raise_exc) as conE: condition = False
        finally: return (true_call if condition else false_call)(*args, **kwargs)
    return(exception_cascade())
