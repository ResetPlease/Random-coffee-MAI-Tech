import pytest
from param_decorator.func_parameter import FuncParameter
from param_decorator.ABC import ParameterCreaterABC
from typing import List, Any
from param_decorator.func_types import CreatingParameterFunction, CreatingParameterGenerator, AsyncCreatingParameterGenerator
from contextlib import _GeneratorContextManager, _AsyncGeneratorContextManager
from inspect import Parameter







class TestFuncParamInit:
    
    
    @staticmethod
    def test_init_only_with_required_parameters(creating_func_without_params) -> None:
        func_param = FuncParameter(ParameterCreaterABC, creating_func_without_params)
        
        assert func_param._creater_class is ParameterCreaterABC
        assert func_param._is_awaitable is False
        assert func_param._name is None
        assert func_param._type is int
        assert isinstance(func_param.get_context_manager(), _GeneratorContextManager)
        assert func_param._func is creating_func_without_params
        assert func_param._func_args == ()
        assert func_param._func_kwargs == {}
        
        
    @staticmethod
    def test_correct_init_creating_func(creating_func) -> None:
        func_args = [(100, 'sring'), (), (100, )]
        func_kwargs = [{}, {'param1' : 100, 'param2' : 'string'}, {'param2' : 'string'}]
        
        for func_args_now, func_kwargs_now in zip(func_args, func_kwargs):
            func_param = FuncParameter(ParameterCreaterABC, creating_func, func_args_now, func_kwargs_now)
            assert func_param._func_args == func_args_now
            assert func_param._func_kwargs == func_kwargs_now
        
        
        
        
    @staticmethod
    def test_init_with_async_creating_func(async_creating_func) -> None:
        func_param = FuncParameter(ParameterCreaterABC, async_creating_func, func_args = (1, 'string'))
        
        assert func_param._creater_class is ParameterCreaterABC
        assert func_param._is_awaitable is True
        assert func_param._name is None
        assert func_param._type is int
        assert isinstance(func_param.get_context_manager(), _AsyncGeneratorContextManager)
        assert func_param._func is async_creating_func
        assert func_param._func_args == (1, 'string')
        assert func_param._func_kwargs == {}
     
          
    @staticmethod
    def test_init_with_incorrect_creater_class(creating_func_without_params) -> None:
        
        for incorrect_creater_class in (str, int, 111, 'sss'):
            with pytest.raises(TypeError):
                FuncParameter(incorrect_creater_class, creating_func_without_params)
        
    
    @staticmethod
    def test_init_with_type_parameter(creating_func_without_annotation) -> None:
        
        for type_ in (str, list[int], TestFuncParamInit, bool):
            func_param = FuncParameter(ParameterCreaterABC, creating_func_without_annotation, func_args = (1, 'string'), type_ = type_)
            assert func_param._type is type_
        


    @staticmethod
    def test_init_with_incorrect_type(creating_func_without_annotation) -> None:
        def first_func_parameter_with_incorrect_annotation() -> List[int]:
            pass
        
        def second_func_parameter_with_incorrect_annotation() -> str:
            pass
        
        for incorrect_type in (None, 100, Any, 'sss'):
            with pytest.raises(TypeError):
                FuncParameter(ParameterCreaterABC, creating_func_without_annotation, func_args = (1, 'string'), type_ = incorrect_type)
            
        with pytest.raises(TypeError):
            FuncParameter(ParameterCreaterABC, first_func_parameter_with_incorrect_annotation)

        with pytest.raises(TypeError):
            FuncParameter(ParameterCreaterABC, second_func_parameter_with_incorrect_annotation)
            
            
    @staticmethod
    def test_init_with_incorrect_generator_type() -> None:
        def first_func() -> CreatingParameterGenerator[Any]:
            yield None
        
        async def second_func() -> AsyncCreatingParameterGenerator[None]:
            yield None
            
            
        with pytest.raises(AttributeError):
            FuncParameter(ParameterCreaterABC, first_func)
            
        with pytest.raises(AttributeError):
            FuncParameter(ParameterCreaterABC, second_func)
            
    
    @staticmethod
    def test_init_with_all_parameters(creating_func_without_annotation) -> None:
        func_param = FuncParameter(ParameterCreaterABC, creating_func_without_annotation, (1,), {'param2' : 'str'}, 'func_param', tuple)
        assert func_param._creater_class is ParameterCreaterABC
        assert func_param._is_awaitable is False
        assert func_param._name == 'func_param'
        assert func_param._type is tuple
        assert isinstance(func_param.get_context_manager(), _GeneratorContextManager)
        assert func_param._func is creating_func_without_annotation
        assert func_param._func_args == (1, )
        assert func_param._func_kwargs == {'param2' : 'str'}
           
        
        




class TestFuncParamWeakmethods:    
    

    
    @staticmethod
    def test_is_weak_correct_type_method() -> None:
        
        for incorrect_type in (Any, None, type(None), 123, 'sss'):
            assert FuncParameter.is_weak_correct_type(incorrect_type) is False
            
        for correct_type in (str, list[str], dict[str, Any], TestFuncParamInit): 
            assert FuncParameter.is_weak_correct_type(correct_type) is True


    @staticmethod
    def test_is_weak_suitable_parameter_method() -> None:
        correct_param_kinds = [Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY]
        incorrect_param_kinds = [Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD]
        
        for correct_kind in correct_param_kinds:
            assert FuncParameter.is_weak_suitable_parameter(Parameter('any', correct_kind)) is True
            assert FuncParameter.is_weak_suitable_parameter(Parameter('any', correct_kind, default = Any)) is False

        for incorrect_kind in incorrect_param_kinds:
            assert FuncParameter.is_weak_suitable_parameter(Parameter('any', incorrect_kind)) is False


    @staticmethod
    def test_is_type_method() -> None:
        correct_types = [
                            (111, int), 
                            ('sss', str), 
                            (TestFuncParamWeakmethods(), TestFuncParamWeakmethods),
                            ([], list[Any]), 
                            ([1, 'sss', []], list[Any]), 
                            ([], list[int]),
                            (['sss', 111, 23, 'sss'], list[str | int]),
                            ([[1, 1, 's'], [2, 2, 'ss'], [], [1]], list[list]),
                            ([[1, 1], [2, 2], [], [1]], list[list[int]]),
                            ({'a' : None, 's' : 'str'}, dict[str, str | None]),
                            ({1 : 1, 2 : 2}, dict[int, int]),
                            ({1 : [11], 2 : [222]}, dict[int, list[int]]),
                            ((1, ), tuple[int]),
                            ((1, 'ss', 1), tuple[int, str, Any]),
                            ((1, 2, 3, 4, 5), tuple[int, ...]),
                            ((None), None),
                            
                            
                        ]
        incorrect_types = [
                            (111, str),
                            ('sss', bool),
                            (TestFuncParamWeakmethods(), TestFuncParamInit),
                            ([], dict[str]),
                            ({'a' : 111}, list[int]),
                            (['sss', 111, 23, 'sss'], list[int]),
                            (['sss', 111, 23, 'sss', None], list[str | int]),
                            ([[1, 1], [2, 2], [], 1], list[list[int]]),
                            ({1 : 1, 2 : 2, 's' : 1}, dict[int, int]),
                            ({1 : 1, 2 : [222]}, dict[int, list[int]]),
                            ((), tuple[int]),
                            ((1, 'ss', 1), tuple[str, str, Any]),
                            ((1, 'ss', 1), tuple[str, str]),
                            ((1, 'ss', 1, 1), tuple[str, str, Any]),
                            ((1, 2, 3, 'sr', 5), tuple[int, ...]),
                            (([None, 1, 2, 3]), list[None])
                        ]
        
        
        for obj, type_ in correct_types:
            assert FuncParameter.is_type(obj, type_) is True
        
        for obj, type_ in incorrect_types:
            assert FuncParameter.is_type(obj, type_) is False
             
        
            
    
    
   

class TestFuncParamMethods:
    
    @staticmethod
    def get_all_variants_is_suitable_parameter(func_param : FuncParameter, name : str, kind, annotation : type | None = None) -> list[bool]:
            return [
                    func_param.is_suitable_parameter(Parameter(name, kind)),
                    func_param.is_suitable_parameter(Parameter(name, kind, annotation = annotation)),
                    func_param.is_suitable_parameter(Parameter(name, kind, default = None)),
                    func_param.is_suitable_parameter(Parameter(name, kind, default = None, annotation = annotation))
                ]
        
        
    
    
    @staticmethod
    def test_is_correct_type_method(creating_func_without_annotation) -> None:
        func_params_types = [str, dict[str, str], TestFuncParamMethods]
        func_params_inccorect_types = [[dict, list[bool], int, bool], [dict, dict[str, int], str], [object, int, list[str]]]
        
        for func_type, incorrect_types in zip(func_params_types, func_params_inccorect_types):
            func_param = FuncParameter(ParameterCreaterABC, creating_func_without_annotation, (1, 'str'), type_ = func_type)
            assert func_param.is_correct_type(Any) is False
            assert func_param.is_correct_type(None) is False
            assert func_param.is_correct_type(func_type) is True
            
            for incorrect_type in incorrect_types:
                assert func_param.is_correct_type(incorrect_type) is False
    
        
    @staticmethod
    def test_is_correct_name_method(creating_func_without_params) -> None:
        func_param_names = [None, 'first', 'func_param', 'created_param']
        func_param_incorrect_names = [['sss', 'qqq', 'ttt'], ['last', 'func_param', 'ss'], ['first', 'func_param_', '_func_param'], ['created', 'param', 'my_param']]

        for name, incorrect_names in zip(func_param_names, func_param_incorrect_names):
            func_param = FuncParameter(ParameterCreaterABC, creating_func_without_params, name = name)
            assert func_param.is_correct_name(name) is (True if name is not None else False)
            assert func_param.is_correct_name(None) is False
            
            for incorrect_name in incorrect_names:
                assert func_param.is_correct_name(incorrect_name) is False
            
          
            
    @classmethod
    def test_is_suitable_parameter_method(cls, creating_func_without_annotation) -> None:
        
        correct_name = 'correct_name'
        correct_func_type = list[int]
        correct_param_kinds = [Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY]
        
        incorrect_param_kinds = [Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD]
        incorrect_types = [int, TestFuncParamInit, list[str], object, dict[str, str]]
        incorrect_names = ['incorrect_name', 'correct_name_1', 'correct_nam']
        
        func_param = FuncParameter(ParameterCreaterABC, creating_func_without_annotation, (1, 'sss'), name = correct_name, type_ = correct_func_type)
        
        for kind, name, type_ in zip(correct_param_kinds, incorrect_names,  incorrect_types):
            assert cls.get_all_variants_is_suitable_parameter(func_param, name, kind, type_) == [False, False, False, False]
            
        for kind, type_ in zip(correct_param_kinds, incorrect_types):
            assert cls.get_all_variants_is_suitable_parameter(func_param, correct_name, kind, type_) == [True, True, False, False]
            
        for kind, name in zip(correct_param_kinds, incorrect_names):
            assert cls.get_all_variants_is_suitable_parameter(func_param, name, kind, correct_func_type) == [False, True, False, False]
        
        for kind in correct_param_kinds:
            assert cls.get_all_variants_is_suitable_parameter(func_param, correct_name, kind, correct_func_type) == [True, True, False, False]

        for kind in incorrect_param_kinds:
            assert func_param.is_suitable_parameter(Parameter(correct_name, kind, annotation = correct_func_type)) is False
            assert func_param.is_suitable_parameter(Parameter(correct_name, kind)) is False
   
    
    
    @classmethod
    def test_is_instance_method(cls, creating_func_without_annotation) -> None:    
        correct_name = 'correct_name'
        correct_func_type = list[int]
        correct_obj = [111, 222, 333]
        
        incorrect_names = ['incorrect_name', 'correct_name_1', 'correct_nam']
        incorrect_objects = [111, 'sss', {'param' : 1}, ['sss', 111]]
        
        func_param = FuncParameter(ParameterCreaterABC, creating_func_without_annotation, (1, 'sss'), name = correct_name, type_ = correct_func_type)
        
        assert func_param.is_instance(correct_obj) is True
        
        for name in incorrect_names:
            assert func_param.is_instance(correct_obj, name) is True
        
        for obj in incorrect_objects:
            assert func_param.is_instance(obj, correct_name) is True
        
        for name, obj in zip(incorrect_names, incorrect_objects):
            assert func_param.is_instance(obj, name) is False
