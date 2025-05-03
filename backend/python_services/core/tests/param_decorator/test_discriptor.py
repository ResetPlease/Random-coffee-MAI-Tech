import pytest
from param_decorator.dicsriptor import ParameterCreater
from param_decorator.func_parameter import FuncParameter
from param_decorator.obj_parameter import SelfParameter, ClassParameter
from inspect import Parameter




@pytest.fixture()
def int_parameter_creater_without_name(creating_func) -> FuncParameter:
    
    return FuncParameter(ParameterCreater, creating_func, (1, 'string'))


@pytest.fixture()
def int_parameter_creater_with_name(creating_func) -> FuncParameter:
    
    return FuncParameter(ParameterCreater, creating_func, (1, 'string'), name = 'param1')


@pytest.fixture()
def core_func_with_params():
    def func(param1 : int, param2 : str) -> int:
        pass
    return func





class TestParameterCreaterInit:
    
    @staticmethod
    def test_valid_init_with_func_without_params() -> None:
        def func_without_params() -> int:
            return 1
        
        param_creater = ParameterCreater(func_without_params)
        
        assert param_creater._core_func is func_without_params
        assert param_creater._core_func_is_awaitable is False
        assert param_creater._func_params == []
        assert param_creater._obj_param is None
        
        
    @staticmethod
    def test_valid_init_with_func_which_has_parameters(core_func_with_params) -> None:
        param_creater = ParameterCreater(core_func_with_params)
        
        assert param_creater._core_func is core_func_with_params
        assert param_creater._core_func_is_awaitable is False
        assert param_creater._func_params == [(Parameter('param1', kind = Parameter.POSITIONAL_OR_KEYWORD, annotation = int), None), (Parameter('param2', kind = Parameter.POSITIONAL_OR_KEYWORD, annotation = str), None)]
        assert param_creater._obj_param is None
        
        
        

class TestParameterCreaterMethods:
    
    @staticmethod
    def test_set_func_parameter_method(
                                        core_func_with_params,
                                        int_parameter_creater_without_name, 
                                        async_creating_func,
                                        creating_func_without_params
                                    ) -> None:

        correct_func_params = [
                                [FuncParameter(ParameterCreater, creating_func_without_params, type_ = str)],
                                [int_parameter_creater_without_name],
                                [
                                    int_parameter_creater_without_name, 
                                    FuncParameter(ParameterCreater, creating_func_without_params, type_ = str)
                                ],
                                [
                                    FuncParameter(ParameterCreater, creating_func_without_params, type_ = bool, name = 'param2'),
                                    int_parameter_creater_without_name
                                ]
                            ]
        
        incorrect_func_params = [
                                    [FuncParameter(ParameterCreater, async_creating_func, (1, 'aaa'))],
                                    [FuncParameter(ParameterCreater, creating_func_without_params, type_ = bool)],
                                    [FuncParameter(ParameterCreater, creating_func_without_params, name = 'param', type_ = bool)],
                                    [
                                        int_parameter_creater_without_name,
                                        int_parameter_creater_without_name
                                    ],
                                    [
                                        FuncParameter(ParameterCreater, creating_func_without_params, type_ = str), 
                                        int_parameter_creater_without_name, 
                                        int_parameter_creater_without_name
                                    ],
                                    [
                                        FuncParameter(ParameterCreater, creating_func_without_params, name = 'param1'), 
                                        int_parameter_creater_without_name
                                    ]
                                    
                                ]
        
        
        for params in correct_func_params:
            param_creater = ParameterCreater(core_func_with_params)
            for param in params:
                param_creater.set_func_parameter(param)
            assert any(func_parameter is not None for (_, func_parameter) in param_creater._func_params) is True
                

        for params in incorrect_func_params:
            with pytest.raises(AttributeError):
                param_creater = ParameterCreater(core_func_with_params)
                for param in params:
                    param_creater.set_func_parameter(param)
            
                    
                
    
    @staticmethod
    def test_attach_method(int_parameter_creater_without_name) -> None:
        
        def func_with_one_param(param1 : int) -> None:
            pass
        def func_with_two_param(param1 : int, param2 : int) -> None:
            pass
        def func_with_three_param(param1 : int, param2 : int, param3 : int) -> None:
            pass
        
        correct_tests = [
                        (func_with_one_param, [SelfParameter(ParameterCreater)]),
                        (func_with_one_param, [ClassParameter(ParameterCreater)]),
                        (func_with_two_param, [SelfParameter(ParameterCreater), int_parameter_creater_without_name]),
                        (func_with_two_param, [int_parameter_creater_without_name, ClassParameter(ParameterCreater)]),
                        (func_with_two_param, [ClassParameter(ParameterCreater)]),
                        (func_with_three_param, [int_parameter_creater_without_name, ClassParameter(ParameterCreater)]),
                        (func_with_three_param, [ClassParameter(ParameterCreater)]),
                        (func_with_three_param, [int_parameter_creater_without_name, int_parameter_creater_without_name, ClassParameter(ParameterCreater)]),
                        (func_with_three_param, [ClassParameter(ParameterCreater), int_parameter_creater_without_name, int_parameter_creater_without_name])
                    ]
        incorrect_tests = [
                        (func_with_one_param, [SelfParameter(ParameterCreater), SelfParameter(ParameterCreater)]),
                        (func_with_two_param, [int_parameter_creater_without_name, SelfParameter(ParameterCreater), int_parameter_creater_without_name, int_parameter_creater_without_name]),
                        (func_with_two_param, [int_parameter_creater_without_name, int_parameter_creater_without_name, SelfParameter(ParameterCreater)]),
                        ]
        
        
        for func, parameters in correct_tests:
            creater = ParameterCreater(func)
            for param in parameters:
                creater.attach(param)
                
            assert creater._obj_param is not None
            assert all((func_param is None or func_param is int_parameter_creater_without_name) for (_, func_param) in creater._func_params)
            
        for func, parameters in incorrect_tests:
            creater = ParameterCreater(func)
            
            with pytest.raises(AttributeError):
                for param in parameters:
                    creater.attach(param)
                    
                    
    
    @staticmethod
    def test_get_func_parameters_need_called(creating_func_without_params) -> None:
        list_param = FuncParameter(ParameterCreater, creating_func_without_params, type_ = list[int])
        int_param = FuncParameter(ParameterCreater, creating_func_without_params, type_ = int)
        multi_param = FuncParameter(ParameterCreater, creating_func_without_params, type_ = str | int)
        
        def default_core_func(param0 : int, param1 : str, param2 : str | int, param3 : list[int]) -> None:
            pass
        
        def core_func_with_args(param0 : int, param1 : str, param2 : str | int, *args, param3 : list[int]):
            pass
        
        def core_func_with_only_pos_args(param0 : int, param1 : str, param2 : str | int, param3 : list[int], /):
            pass
        
        def core_func_with_only_kw_args(*,param0 : int, param1 : str, param2 : str | int, param3 : list[int]):
            pass
        
        tests = [
            (default_core_func, (list_param,), [1, 'ss', 'ss'], {}, ([], [3])),
            (default_core_func, (list_param,), [1, 'ss', 'ss', [1]], {}, ([], [])),
            (default_core_func, (list_param,), [1, 'ss', 'sss'], {'param3' : []}, ([], [])),
            (default_core_func, (list_param,), [], {'param0' : 1, 'param2' : 1, 'param1' : 'sss'}, ([], [3])),
            (default_core_func, (list_param,), [], {'param0' : 1, 'param2' : 1, 'param1' : 'sss', 'param3' : [1]}, ([], [])),
            (default_core_func, (list_param, int_param), [1, 'ss', 'sss'], {}, ([], [3])),
            (default_core_func, (list_param, int_param), ['sss', 1, []], {}, ([0], [])),
            (default_core_func, (list_param, int_param), ['sss', 1], {}, ([0], [3])),
            (default_core_func, (list_param, int_param), [], {'param2': 1, 'param1': 'sss'}, ([], [0, 3])),
            (default_core_func, (list_param, multi_param), [], {'param0': 1, 'param1': 'sss'}, ([], [2, 3])),
            (default_core_func, (list_param, multi_param, int_param), [1, 'ss'], {'param3': []}, ([], [2])),
            (default_core_func, (list_param, multi_param, int_param), ['ss'], {}, ([0], [2, 3])),
            (core_func_with_args, (multi_param, ), [1, 'sss'], {'param3' : [111]}, ([], [2])),
            (core_func_with_args, (multi_param, ), [1, 'sss', [], 1111, 111], {'param3' : [111]}, ([2], [])),
            (core_func_with_only_pos_args, (list_param, multi_param, int_param), ['sss'], {}, ([0, 2, 3], [])),
            (core_func_with_only_pos_args, (list_param, multi_param, int_param), ['sss', 'ss'], {}, ([0, 3], [])),
            (core_func_with_only_kw_args, (list_param, multi_param, int_param), [], {'param1' : 'ss'}, ([], [0, 2, 3])),
            (core_func_with_only_kw_args, (list_param, multi_param, int_param), [], {'param1' : 'ss', 'param2' : 'ss'}, ([], [0, 3]))
           
        ]
        
        for (core_func, func_params, args, kwargs, needed_args_kwargs) in tests:
            creater = ParameterCreater(core_func)
            for param in func_params:
                creater.attach(param)
            
            assert creater.get_func_parameters_need_called(args, kwargs) == needed_args_kwargs
        
        
        
    
    @staticmethod
    def test_get_concatinated_args_with_func_params() -> None:
        
        tests = [
                ([1, 2, 3], ['a', 'b'], [1, 3], [1, 'a', 2, 3, 'b']),
                ([1, 2], ['a'], [0], ['a', 1, 2]),
                ([], ['a'], [0], ['a']),
                ([1, 2], ['a', 'b'], [2, 3], [1, 2, 'a', 'b']),
                ([1, 2, 3], ['a', 'b'], [0, 2], ['a', 1, 2, 'b', 3]),
                ([1, 2], [], [], [1, 2]),
                (['x'], [100], [0], [100, 'x']),
                (['x', 'y'], [True], [2], ['x', 'y', True]),
                ([], ['a', 'b'], [0, 1], ['a', 'b'])
            ]
        
        for (args, func_params, indexes, result) in tests:
            assert ParameterCreater.get_concatinated_args_with_func_params(args, func_params, indexes) == result
        
        
    @staticmethod
    def test_get_concatinated_kwargs_with_func_params() -> None:
        tests = [
            ({}, (), [], {}),
            ({'a': 1}, (2, 3), ['b', 'c'], {'a': 1, 'b': 2, 'c': 3}),
            ({'a': 1, 'b': 2}, (10, 20), ['a', 'b'], {'a': 10, 'b': 20}),
            ({}, (1, 2, 3), ['a', 'b'], {'a': 1, 'b': 2}),
            ({'a' : 1}, (), [], {'a' : 1})
        ]

        for (kwargs, func_params, names, result) in tests:
            assert ParameterCreater.get_concatinated_kwargs_with_func_params(kwargs, func_params, names) == result
        
        
            

class TestFuncCreaterCall:
    instance, owner = TestParameterCreaterInit(), TestParameterCreaterInit     
    self_param = SelfParameter(ParameterCreater)
    class_param = ClassParameter(ParameterCreater)
        
    func_for_generate_tests = lambda list_param, int_param, multi_param : [
                ((list_param,), [1, 2], {'param4' : 4}, (1, 2, [1, 2, 3], 4)),
                ((list_param,), [1, 2], {'param4' : 4, 'param3' : [1, 1]}, (1, 2, [1, 1], 4)),
                ((list_param, TestFuncCreaterCall.class_param), [2], {'param4' : 4}, (TestFuncCreaterCall.owner, 2, [1, 2, 3], 4)),
                ((TestFuncCreaterCall.self_param, list_param), [2], {'param4' : 4}, (TestFuncCreaterCall.instance, 2, [1, 2, 3], 4)),
                ((TestFuncCreaterCall.self_param, list_param), [2], {'param4' : 4, 'param3' : [1, 1]}, (TestFuncCreaterCall.instance, 2, [1, 1], 4)),
                ((TestFuncCreaterCall.self_param, list_param, int_param, multi_param), [], {}, (TestFuncCreaterCall.instance, 'sss', [1, 1], 123)),
                ((TestFuncCreaterCall.class_param, list_param, int_param, multi_param), [], {'param4' : 4, 'param3' : [1, 1]}, (TestFuncCreaterCall.owner, 'sss', [1, 1], 4)),
                ((TestFuncCreaterCall.class_param, list_param, int_param, multi_param), [123], {}, (TestFuncCreaterCall.owner, 123, [1, 1], 123)),
                ((TestFuncCreaterCall.class_param, list_param, int_param, multi_param), ['www'], {'param4' : 1000, 'param3' : [1, 100]}, (TestFuncCreaterCall.owner, 'www', [1, 100], 1000)),
            ]
    
    @classmethod
    def test_synchronous_call_core_func(cls) -> None:
        def list_func_param():
            yield [1, 2, 3]
        
        def int_func_param():
            yield 123
            
        def str_or_int_param():
            yield 'sss'
            
        list_param = FuncParameter(ParameterCreater, list_func_param, type_ = list[int])
        int_param = FuncParameter(ParameterCreater, int_func_param, type_ = int)
        multi_param = FuncParameter(ParameterCreater, str_or_int_param, type_ = str | int)
        
        def core_func(param1, param2 : str | int, *, param3 : list[int], param4 : int):
            return param1, param2, param3, param4
        
        tests = cls.func_for_generate_tests(list_param, int_param, multi_param)
        
        for func_params, args, kwargs, result in tests:
            creater = ParameterCreater(core_func)
            for param in func_params:
                creater.attach(param)
            
            creater.synchronous_call_core_func(TestFuncCreaterCall.instance, TestFuncCreaterCall.owner)(*args, **kwargs) == result
            
    
    @classmethod
    @pytest.mark.asyncio()
    async def test_asynchronous_call_core_func(cls) -> None:
        async def list_func_param():
            yield [1, 2, 3]
        
        async def int_func_param():
            yield 123
            
        async def str_or_int_param():
            yield 'sss'
            
        list_param = FuncParameter(ParameterCreater, list_func_param, type_ = list[int])
        int_param = FuncParameter(ParameterCreater, int_func_param, type_ = int)
        multi_param = FuncParameter(ParameterCreater, str_or_int_param, type_ = str | int)
        
        async def core_func(param1, param2 : str | int, *, param3 : list[int], param4 : int):
            return param1, param2, param3, param4
        
        tests = cls.func_for_generate_tests(list_param, int_param, multi_param)
        
        for func_params, args, kwargs, result in tests:
            creater = ParameterCreater(core_func)
            for param in func_params:
                creater.attach(param)
            
            returning = await creater.asynchronous_call_core_func(TestFuncCreaterCall.instance, TestFuncCreaterCall.owner)(*args, **kwargs)
            returning == result
    
    