__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-05-07"
__version__ = "0.0.0"

from json import dump as json_dump, load as json_load, dumps as json_dumps, loads as json_loads
from json
from dill import dump as dill_dump, load as dill_load, dumps as dill_dumps, loads as dill_loads,\
    HIGHEST_PROTOCOL, PicklingError, UnpicklingError


class DumpError(Exception):
    def __init__(self, cls): super(DumpError, self).__init__(f'{cls}: serialization failed')
    
    
class LoadError(Exception):
    def __init__(self, cls): super(LoadError, self).__init__(f'{cls}: deserialization failed')
    
    
class json:
    @staticmethod
    def dumpFile(path, saveObj, **kwargs):
        try:
            with path.open('wb+') as sfile: json_dump(saveObj, sfile, **kwargs)
        except (TypeError,): raise DumpError(json.__name__)

    @staticmethod
    def loadFile(path, **kwargs):
        try:
            with path.open('rb') as lfile: return json_load(lfile, **kwargs)
        except (TypeError,): raise LoadError(json.__name__)

    @staticmethod
    def dumpObject(obj, **kwargs):
        try: return json_dumps(obj, **kwargs)
        except (TypeError,): raise DumpError(json.__name__)

    @staticmethod
    def loadObject(obj, **kwargs):
        try: return json_loads(obj, **kwargs)
        except (TypeError,): raise LoadError(json.__name__)

    
class dill:
    @staticmethod
    def dumpFile(path, saveObj):
        try:
            with path.open('wb+') as sfile: dill_dump(saveObj, sfile, HIGHEST_PROTOCOL)
        except (UnpicklingError,): raise DumpError(dill.__name__)

    @staticmethod
    def loadFile(path):
        try:
            with path.open('rb') as lfile: return dill_load(lfile)
        except (PicklingError,): raise LoadError(dill.__name__)

    @staticmethod
    def dumpObject(obj):
        try: return dill_dumps(obj, HIGHEST_PROTOCOL)
        except (PicklingError,): raise DumpError(dill.__name__)

    @staticmethod
    def loadObject(obj):
        try: return dill_loads(obj)
        except (UnpicklingError,): raise LoadError(dill.__name__)



if __name__ == '__main__': pass
