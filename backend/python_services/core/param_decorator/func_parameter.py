from typing import Callable, Any, Generator, AsyncGenerator, Iterable, Mapping
from .func_types import (
                        ParameterType, 
                        CreatingParameterFuncParams,
                        CreatingParameterFunction        
                    )
from .ABC import FuncParameterABC, FuncParameterBuilderABC, ParameterCreaterABC
from functools import wraps
from inspect import isasyncgenfunction, Parameter, iscoroutinefunction
from contextlib import _GeneratorContextManager, _AsyncGeneratorContextManager
from .abstract_parameter import AbstractParameter
from types import GenericAlias, UnionType

        

class FuncParameter(AbstractParameter, FuncParameterABC):
    
    __slots__ = ()
    
    def __init__(
                    self,
                    creater_class : type[ParameterCreaterABC],
                    creating_func : CreatingParameterFunction[CreatingParameterFuncParams, ParameterType],
                    func_args : tuple[Any] | None = None,
                    func_kwargs : dict[str, Any] | None = None,
                    name : str | None = None,
                    type_ : type | None = None
                ) -> None:
        self._creater_class = creater_class
        self._is_awaitable = isasyncgenfunction(creating_func) or iscoroutinefunction(creating_func)
        self._name = name
        self._type = type_
        self._func = creating_func
        self._func_args = func_args or ()
        self._func_kwargs = func_kwargs or {}
        
        
        if not issubclass(creater_class, ParameterCreaterABC):
            raise TypeError('The creater_class is not subclass of ParameterCreaterABC')
        
        
        if self.is_weak_correct_type(self._type):
            return
        
        self._type = creating_func.__annotations__.get('return')
        
        if not getattr(self._type, '__origin__', None) or not issubclass(self._type.__origin__, (AsyncGenerator, Generator)):
            raise TypeError('The parameter must have an annotation type Generator or AsyncGenerator')
        
        self._type = self._type.__args__[0]
        
        if not self.is_weak_correct_type(self._type):
            raise AttributeError('The parameter must be named or have a type other than None or Any')
      
      
    @staticmethod
    def is_weak_correct_type(type_ : type) -> bool:
        return type_ not in (Any, None, type(None)) and isinstance(type_, (type, GenericAlias, UnionType))
    
    
    def is_correct_type(self, type_ : type) -> bool:
        return self.is_weak_correct_type(type_) and type_ == self._type
    
    
    def is_correct_name(self, name : str | None) -> bool:
        return self._name is not None and self._name == name
    
        
    
    def is_awaitable(self) -> bool:
        return self._is_awaitable
    
    
    
    def __repr__(self) -> str:
        return  f'{self.__class__.__name__}'\
                f'(name={self._name},type={self._type},'\
                f'func={self._func.__name__}'\
                f',func_args={self._func_args},'\
                f'func_kwargs={self._func_kwargs})'
       
     
    @staticmethod  
    def is_weak_suitable_parameter(parameter : Parameter) -> bool:
        return parameter.kind not in (Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL) and parameter.default == Parameter.empty
     
        
    def is_suitable_parameter(self, parameter : Parameter) -> bool:  
        return self.is_weak_suitable_parameter(parameter) and (self.is_correct_type(parameter.annotation) or self.is_correct_name(parameter.name))
    
    
    def get_context_manager(self) -> _GeneratorContextManager | _AsyncGeneratorContextManager:
        if self.is_awaitable():
            return _AsyncGeneratorContextManager(self._func, self._func_args, self._func_kwargs)
        return _GeneratorContextManager(self._func, self._func_args, self._func_kwargs)
    
    
    @classmethod
    def is_type(cls, obj : Any, type_ : type) -> bool:
        origin = getattr(type_, '__origin__', None)
        args = getattr(type_, '__args__', ())
        
        
        if type_ is None:
            return obj is None
        
        if origin is None:
            return type_ is Any or isinstance(obj, type_)
        
        if not isinstance(obj, origin):
            return False
        
        if isinstance(obj, tuple):
            if ... in args:
                value_type = args[0]
                return all(cls.is_type(value, value_type) for value in obj)
            
            return len(obj) == len(args) and all(
                cls.is_type(value, value_type) for value, value_type in zip(obj, args)
            )
            
        
        if isinstance(obj, Mapping):
            key_type, value_type = args[0], args[1]
            return all(cls.is_type(key, key_type) and cls.is_type(value, value_type) for key, value in obj.items())
        
        
        if isinstance(obj, Iterable):
            value_type = args[0]
            return all(cls.is_type(value, value_type) for value in obj)
        
        return True
        
    
    
    
    def is_instance(
                    self,
                    obj : Any,
                    obj_name : str | None = None
                ) -> bool:  
        
        return self.is_type(obj, self._type) or self.is_correct_name(obj_name)
    
    
    
    

class FuncParameterBuilder(FuncParameterBuilderABC):
    
    __slots__ = ()
    
    
    def __init__(
                self,
                discriptor_class : type[ParameterCreaterABC],
                param_name : str | None = None,
                param_type : type | None = None
            ) -> None:
        self.discriptor_class = discriptor_class
        self.param_name = param_name
        self.param_type = param_type
        
    
    
    def __call__(
                    self,
                    func : CreatingParameterFunction[CreatingParameterFuncParams, ParameterType]
                ) -> Callable[CreatingParameterFuncParams, FuncParameter]:
        
        @wraps(func)
        def create_discriptor_classwith_args(*args, **kwargs) -> FuncParameter:
            return FuncParameter(self.discriptor_class, func, args, kwargs, self.param_name, self.param_type)
        
        return create_discriptor_classwith_args
    
    
    
    
            
            

    
    