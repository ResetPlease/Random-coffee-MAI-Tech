import pytest
from param_decorator.obj_parameter import SelfParameter, ClassParameter
from param_decorator.ABC import ParameterCreaterABC



class MockObject:
    pass




class TestObjParamInit:
    


    @staticmethod
    def test_valid_init() -> None:
        
        self_param, class_param = SelfParameter(ParameterCreaterABC), ClassParameter(ParameterCreaterABC)
        
        assert self_param._creater_class is ParameterCreaterABC
        assert class_param._creater_class is ParameterCreaterABC
    
    

class TestObjMethods:
    
    
    @staticmethod
    def test_get_parameter() -> None:
        obj, class_ = MockObject(), MockObject
        
        assert SelfParameter.get_parameter(obj, class_) is obj
        assert ClassParameter.get_parameter(obj, class_) is class_ 