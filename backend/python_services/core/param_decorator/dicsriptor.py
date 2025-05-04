from .ABC import ParameterCreaterABC, FuncParameterABC, ObjectParameterABC
from inspect import iscoroutinefunction, signature, Parameter
from functools import wraps
from typing import Any, Coroutine, Callable
from .func_types import CoreFunction
from contextlib import ExitStack, AsyncExitStack
import asyncio



class ParameterCreater[**CoreFuncParams, CoreFuncReturnType](ParameterCreaterABC):
    
    
    def __init__(self, core_func : CoreFunction[CoreFuncParams, CoreFuncReturnType]) -> None:
        self._core_func = core_func
        self._core_func_is_awaitable = iscoroutinefunction(core_func)
        self._func_params : list[tuple[Parameter, FuncParameterABC | None]] = [(param, None) for param in signature(core_func).parameters.values()]
        self._obj_param : ObjectParameterABC | None = None
    
    
    
    def set_obj_parameter(self, parameter : ObjectParameterABC) -> None:
        if self._obj_param is not None:
            raise AttributeError('Double initialization ObjectParameter')
        
        self._obj_param = parameter
        (_, func_parameter), *self._func_params = self._func_params

        if func_parameter is not None:
            return self.set_func_parameter(func_parameter)
    
        
        
    def set_func_parameter(self, parameter : FuncParameterABC) -> None:
        
        if self._core_func_is_awaitable != parameter.is_awaitable():
            raise AttributeError('All functions must be either synchronous or asynchronous')  
        
        for index, (param, func_param_now) in enumerate(self._func_params):
            if func_param_now is None and parameter.is_suitable_parameter(param):
                self._func_params[index] = (param, parameter)
                return 
        
        raise AttributeError(f'It is impossible to determine the parameter {parameter} of the function {self._core_func.__name__}')
        
    
    
    
    def attach(self, parameter : FuncParameterABC | ObjectParameterABC) -> None:
        
        if isinstance(parameter, ObjectParameterABC):
            self.set_obj_parameter(parameter)
            return 
        
        self.set_func_parameter(parameter)
        
    
    def get_func_parameters_need_called(
                                            self, 
                                            args : tuple[Any, ...],
                                            kwargs : dict[str, Any]
                                        ) -> tuple[list[int], list[int]]:
        func_parameters_in_args : list[int] = []
        func_parameters_in_kwargs : list[int] = []
        current_arg_index = 0
        
        
        for param_index in range(len(self._func_params)):
            param, func_param = self._func_params[param_index]
           
            if current_arg_index >= len(args) or param.kind not in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
                break

            current_arg = args[current_arg_index]
            if func_param is not None and not func_param.is_instance(current_arg):
                func_parameters_in_args.append(param_index)
                continue
            
            current_arg_index += 1
            
        else:
            param_index += 1

 
        for param_index in range(param_index, len(self._func_params)):
            param, func_param = self._func_params[param_index]
            
            if param.kind != Parameter.POSITIONAL_ONLY:
                break
            
            if func_param is not None:
                func_parameters_in_args.append(param_index)
        
        else:
            param_index += 1
                
            
        
        for param_index in range(param_index, len(self._func_params)):
            param, func_param = self._func_params[param_index]
            
            if (
                kwargs.get(param.name) is None and 
                param.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY) and
                func_param is not None
            ):
                func_parameters_in_kwargs.append(param_index)
        
        return func_parameters_in_args, func_parameters_in_kwargs



    @staticmethod
    def get_concatinated_args_with_func_params(
                                            args : tuple[Any, ...], 
                                            func_params : tuple[Any, ...], 
                                            func_params_indexes : list[int]
                                        ) -> list[Any]:
        processed_args : list[Any] = []
        current_arg_index = 0
        
        for param_index, func_param in zip(func_params_indexes, func_params):
            processed_args.extend(args[current_arg_index : param_index])
            processed_args.append(func_param)
            current_arg_index = param_index
        
        processed_args.extend(args[current_arg_index :])
        
        return processed_args
    
    
    @staticmethod
    def get_concatinated_kwargs_with_func_params(
                                                    kwargs : dict[str, Any],
                                                    func_params : tuple[Any, ...],
                                                    func_params_names : list[str]
                                                ) -> dict[str, Any]:
        processed_kwargs : dict[str, Any] = kwargs.copy()
        for param_name, func_param_value in zip(func_params_names, func_params):
            processed_kwargs[param_name] = func_param_value
        
        return processed_kwargs
            
            
        
        
        
        
        
    
    def synchronous_call_core_func(self, instance : object | None, owner : type[object] | None) -> Callable[CoreFuncParams, CoreFuncReturnType]:
        
        @wraps(self._core_func)
        def wrapper(*args, **kwargs) -> CoreFuncReturnType:
            func_params_args_indexes, func_params_kwargs_indexes = self.get_func_parameters_need_called(args, kwargs)
            
            with ExitStack() as func_stack:
                
                func_args_params = tuple(func_stack.enter_context(self._func_params[index][1].get_context_manager()) for index in func_params_args_indexes)
                func_kwargs_params = tuple(func_stack.enter_context(self._func_params[index][1].get_context_manager()) for index in func_params_kwargs_indexes)
                concatinated_args = self.get_concatinated_args_with_func_params(args, func_args_params, func_params_args_indexes)
                concatinated_kwargs = self.get_concatinated_kwargs_with_func_params(kwargs, func_kwargs_params, [self._func_params[index][0].name for index in func_params_kwargs_indexes])
                
                if self._obj_param:
                    return self._core_func(self._obj_param.get_parameter(instance, owner), *concatinated_args, **concatinated_kwargs)

                return self._core_func(*concatinated_args, **concatinated_kwargs)

        return wrapper
            
        
    
    
    def asynchronous_call_core_func(self, instance : object | None, owner : type[object] | None) -> Coroutine[None, None, CoreFuncReturnType]:
        
        @wraps(self._core_func)
        async def wrapper(*args, **kwargs) -> CoreFuncReturnType:
            func_params_args_indexes, func_params_kwargs_indexes = self.get_func_parameters_need_called(args, kwargs)
            
            async with AsyncExitStack() as func_stack:
                func_args_params, func_kwargs_params = await asyncio.gather(
                    asyncio.gather(*[func_stack.enter_async_context(self._func_params[index][1].get_context_manager()) for index in func_params_args_indexes]),
                    asyncio.gather(*[func_stack.enter_async_context(self._func_params[index][1].get_context_manager()) for index in func_params_kwargs_indexes])
                )
                           
                concatinated_args = self.get_concatinated_args_with_func_params(args, func_args_params, func_params_args_indexes)
                concatinated_kwargs = self.get_concatinated_kwargs_with_func_params(kwargs, func_kwargs_params, [self._func_params[index][0].name for index in func_params_kwargs_indexes])
                
                if self._obj_param:
                    return await self._core_func(self._obj_param.get_parameter(instance, owner), *concatinated_args, **concatinated_kwargs)

                return await self._core_func(*concatinated_args, **concatinated_kwargs)

        return wrapper
        
    
    def __get__(self, instance : object | None, owner : type[object] | None = None) -> Callable[CoreFuncParams, CoreFuncReturnType]: 
        
        if self._core_func_is_awaitable:
            return self.asynchronous_call_core_func(instance, owner)
        
        return self.synchronous_call_core_func(instance, owner)
        
        
        
        
        