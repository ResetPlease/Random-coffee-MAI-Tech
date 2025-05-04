from typing import Callable, Generator, TypeAlias, TypeVar, ParamSpec, AsyncGenerator

ParameterType = TypeVar('ParameterType')
CreatingParameterFuncParams = ParamSpec('CreatingParameterFuncParams')
CoreFuncReturnType = TypeVar('CoreFuncReturnType')
CoreFuncParams = ParamSpec('CoreFuncParams')


CreatingParameterGenerator : TypeAlias = Generator[ParameterType, None, None]
AsyncCreatingParameterGenerator : TypeAlias = AsyncGenerator[ParameterType, None]
CreatingParameterFunction : TypeAlias = Callable[CreatingParameterFuncParams, CreatingParameterGenerator[ParameterType] | AsyncCreatingParameterGenerator[ParameterType]]
CoreFunction : TypeAlias = Callable[CoreFuncParams, CoreFuncReturnType]
