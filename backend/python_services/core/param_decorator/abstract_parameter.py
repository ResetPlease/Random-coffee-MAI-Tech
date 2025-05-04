from .func_types import (
                        CoreFunction,
                        CoreFuncParams,
                        CoreFuncReturnType
                    )
from .ABC import AbstractParameterABC, ParameterCreaterABC



class AbstractParameter(AbstractParameterABC):
    
    __slots__ = ()
    
    def __init__(
                    self,
                    creater_class : type[ParameterCreaterABC]
                ) -> None:
        self._creater_class = creater_class
        
        
    def __call__(
                    self,
                    func_or_creater : CoreFunction[CoreFuncParams, CoreFuncReturnType] | ParameterCreaterABC[CoreFuncParams, CoreFuncReturnType]
                ) -> ParameterCreaterABC[CoreFuncParams, CoreFuncReturnType]:
        creater = func_or_creater if isinstance(func_or_creater, self._creater_class) else self._creater_class(func_or_creater)
        creater.attach(self)
        return creater
        