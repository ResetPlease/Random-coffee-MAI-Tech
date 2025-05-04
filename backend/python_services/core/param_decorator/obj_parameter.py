from .ABC import ObjectParameterABC, ParameterCreaterABC
from .func_types import (
                        CoreFuncReturnType,
                        CoreFuncParams,
                        CoreFunction
                    )
from typing import Concatenate, Any
from .abstract_parameter import AbstractParameter



class ObjectParameter(AbstractParameter, ObjectParameterABC):
    
    __slots__ = ()
    
    
    def __call__[SelfOrClass](
                    self,
                    func_or_creater : CoreFunction[Concatenate[SelfOrClass, CoreFuncParams], CoreFuncReturnType] | ParameterCreaterABC[Concatenate[SelfOrClass, CoreFuncParams], CoreFuncReturnType]
                ) -> ParameterCreaterABC[CoreFuncParams, CoreFuncReturnType]:
        return super().__call__(func_or_creater)
    
    

class SelfParameter(ObjectParameter):
    
    __slots__ = ()
    
    
    @staticmethod
    def get_parameter(instance : object | None, owner : type[object] | None) -> object | type:
        return instance
    

    
class ClassParameter(ObjectParameter):
    
    __slots__ = ()
    
    @staticmethod
    def get_parameter(instance : object | None, owner : type[object] | None) -> object | type:
        return owner
    
    
