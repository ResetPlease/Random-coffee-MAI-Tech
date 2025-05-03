from typing import Callable, Any, Coroutine, Concatenate
from abc import abstractmethod, ABC
from .func_types import (
                        CreatingParameterFuncParams,
                        ParameterType,
                        CreatingParameterFunction,
                        CoreFunction,
                        CoreFuncParams,
                        CoreFuncReturnType
                    )
from inspect import Parameter
from contextlib import _GeneratorContextManager, _AsyncGeneratorContextManager 


class ParameterCreaterABC[**CoreFuncParams, CoreFuncReturnType](ABC):
    
    
    @abstractmethod
    def __init__(self, core_func : CoreFunction[CoreFuncParams, CoreFuncReturnType]) -> None:
        ...
        
        
    @abstractmethod
    def attach(self, parameter : 'AbstractParameterABC') -> None:
        ...
        
        
    @abstractmethod
    def synchronous_call_core_func(self, instance : object | None, owner : type[object] | None = None) -> Callable[CoreFuncParams, CoreFuncReturnType]:
        ...
        
    
    @abstractmethod
    def asynchronous_call_core_func(self, instance : object | None, owner : type[object] | None = None) -> Callable[CoreFuncParams, CoreFuncReturnType]:
        ...
        
        
    @abstractmethod
    def __get__(self, instance : object | None, owner : type[object] | None = None) -> Callable[CoreFuncParams, CoreFuncReturnType]:
        ... 
        
        
    @abstractmethod
    def get_func_parameters_need_called(
                                        self,
                                        args : tuple[Any],
                                        kwargs : dict[str, Any]
                                    ) -> tuple[list[int], list[int]]:
        ...
        


class AbstractParameterABC(ABC):
    
    __slots__ = ('_creater_class', )
   

    @abstractmethod
    def __init__(
                    self,
                    creater_class : type[ParameterCreaterABC]
                ) -> None:
        ...
        
        
    @abstractmethod
    def __call__(
                    self,
                    func_or_creater : CoreFunction[CoreFuncParams, CoreFuncReturnType] | ParameterCreaterABC[CoreFuncParams, CoreFuncReturnType]
                ) -> ParameterCreaterABC[CoreFuncParams, CoreFuncReturnType]:
        ...
        

        
class ObjectParameterABC(AbstractParameterABC):
    
    __slots__ = ()
        
    
    @staticmethod
    @abstractmethod
    def get_parameter(instance : object | None, owner : type[object] | None) -> object | type:
        ...
    
    
    @abstractmethod
    def __call__[SelfOrClass](
                    self,
                    func_or_creater : CoreFunction[Concatenate[SelfOrClass, CoreFuncParams], CoreFuncReturnType] | ParameterCreaterABC[Concatenate[SelfOrClass, CoreFuncParams], CoreFuncReturnType]
                ) -> ParameterCreaterABC[CoreFuncParams, CoreFuncReturnType]:
        ...


        
        

class FuncParameterABC(AbstractParameterABC):
    
    __slots__ = ('_is_awaitable', '_name', '_type', '_func', '_func_args', '_func_kwargs')
    
    
    @abstractmethod
    def __init__(
                    self,
                    creater_class : type[ParameterCreaterABC],
                    creating_func : CreatingParameterFunction[CreatingParameterFuncParams, ParameterType],
                    func_args : tuple[Any] | None = None,
                    func_kwargs : dict[str, Any] | None = None,
                    name : str | None = None,
                    type_ : type | None = None
                ) -> None:
        ...
        
    @staticmethod
    @abstractmethod
    def is_correct_type(type_ : type) -> bool:
        ...
        
        
    @abstractmethod
    def is_weak_correct_type(self, type_ : type) -> bool:
        ...
        
    
    @abstractmethod
    def is_correct_name(self, name : str | None) -> bool:
        ...
        
        
    @abstractmethod
    def is_awaitable(self) -> bool:
        ...
        
    
    @staticmethod    
    @abstractmethod
    def is_weak_suitable_parameter(self, parameter : Parameter) -> bool:
        ...
        
        
    @abstractmethod
    def is_suitable_parameter(self, parameter : Parameter) -> bool:
        ...
    
    
    @abstractmethod
    def __repr__(self) -> str:
        ...
    
    
    @abstractmethod
    def get_context_manager(self) -> _GeneratorContextManager | _AsyncGeneratorContextManager:
        ...
        
    
    @classmethod
    @abstractmethod
    def is_type(cls, obj : Any, type_ : type) -> bool:
        ...
        
        
    @abstractmethod
    def is_instance(
                    self,
                    obj : Any,
                    obj_name : str | None = None
                ) -> bool:
        ...
    
    
    
    
    


class FuncParameterBuilderABC(ABC):
    
    
    __slots__ = ('discriptor_class', 'param_name', 'param_type')
    
    
    @abstractmethod
    def __init__(
                self,
                discriptor_class : type[ParameterCreaterABC],
                param_name : str | None = None,
                param_type : type | None = None
            ) -> None:
        ...
        
    
    @abstractmethod
    def __call__(
                self,
                func : CreatingParameterFunction[CreatingParameterFuncParams, ParameterType]
            ) -> Callable[CreatingParameterFuncParams, FuncParameterABC]:
        ...
            
            
        
        