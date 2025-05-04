import pytest
from param_decorator.func_types import CreatingParameterFunction, CreatingParameterGenerator, AsyncCreatingParameterGenerator
from typing import Any


@pytest.fixture()
def creating_func() -> CreatingParameterFunction[[int, str], int]:
    def mock_func(param1 : int, param2 : str) -> CreatingParameterGenerator[int]:
        yield param1, param2
        
    return mock_func



@pytest.fixture()
def creating_func_without_params() -> CreatingParameterFunction[[], int]:
    def mock_func() -> CreatingParameterGenerator[int]:
        yield 'mock'
        
    return mock_func



@pytest.fixture()
def creating_func_without_annotation() -> CreatingParameterFunction[[int, str], Any]:
    def mock_func(param1 : int, param2 : str):
        yield param1, param2
        
    return mock_func



@pytest.fixture()
def async_creating_func() -> CreatingParameterFunction[[int, str], int]:
    async def mock_func(param1 : int, param2 : str) -> AsyncCreatingParameterGenerator[int]:
        yield param1, param2
        
    return mock_func
