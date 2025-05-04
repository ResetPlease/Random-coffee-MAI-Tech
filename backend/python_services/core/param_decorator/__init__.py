from .func_types import (
                        ParameterType, 
                        CreatingParameterFuncParams,
                        CreatingParameterFunction,
                        CreatingParameterGenerator,
                        AsyncCreatingParameterGenerator,
                        CoreFuncParams,
                        CoreFuncReturnType,
                        CoreFunction
                    )
from .dicsriptor import ParameterCreater
from .func_parameter import FuncParameterBuilder
from .obj_parameter import SelfParameter, ClassParameter



def func_parameter(
                    name : str | None = None,
                    type : type | None = None
                ) -> FuncParameterBuilder:
    return FuncParameterBuilder(ParameterCreater, name, type)


def class_parameter() -> ClassParameter:
    return ClassParameter(ParameterCreater)

def self_parameter() -> SelfParameter:
    return SelfParameter(ParameterCreater)


        
