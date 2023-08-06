
import types
from typing import Union

def validate(func, locals):
    for var, test in func.__annotations__.items():

        try:
            test = test.__args__
            _test_msg = " or ".join(map(str,test))
        except:
            test = test
            _test_msg  = test

        value = locals[var]
        msg = f"Error in {func}: {var} argument must be {_test_msg}"
        assert isinstance(value,test),msg

def sum(a:int,b:int=2):
    validate(sum, locals())
    return a,b

class SUM():
    def __init__(self,b:Union[int,str],a:int):
        # print(locals())
        # print(locals())
        validate(self.__init__, locals())
        # return a,b

# sum("2",3)
SUM(a=2,b=[5])
# print(type(SUM))
# print(type(sum))