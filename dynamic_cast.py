from typing import ParamSpec, TypeVar, Any, overload
from collections.abc import Callable, Awaitable; from collections import OrderedDict
from types import MappingProxyType
import functools; import inspect

P = ParamSpec("P")
R = TypeVar("R")
ARGUMENT = TypeVar("ARGUMENT", bound=Any)
ANNOTATION = TypeVar("ANNOTATION", bound=type)

@overload
def dynamic_cast(func_: Callable[P, R], *, strict: bool = ..., cast_impl: Callable[[Any, type], Any] | None = None)\
    -> Callable[..., R]: ...

@overload
def dynamic_cast(func_: None = None, *, strict: bool = ..., cast_impl: Callable[[Any, type], Any] | None = None)\
    -> Callable[[Callable[P, R]], Callable[..., R]]: ...

def dynamic_cast(func_: Callable[P, R] | None = None, *, strict: bool = False, cast_impl: Callable[[Any, type], Any] | None = None)\
    -> Callable[..., R] | Callable[[Callable[P, R]], Callable[..., R]]:
    if strict: raise NotImplementedError
    def dynamic_cast_impl_(argument: ARGUMENT, annotation: ANNOTATION) -> ANNOTATION:
        if isinstance(argument, str) and annotation is int:
            return annotation(float(argument))
        elif annotation in (inspect.Parameter.empty, inspect.Signature.empty):
            return argument
        else:
            return annotation(argument)
    def decorator_dynamic_cast(func: Callable[P, R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper_dynamic_cast(*args: Any, **kwargs: Any) -> R:
            cast_impl_ = cast_impl or dynamic_cast_impl_
            signature: inspect.Signature = inspect.signature(func)
            parameters: MappingProxyType[str, inspect.Parameter] = signature.parameters
            bind: inspect.BoundArguments = signature.bind(*args, **kwargs)
            arguments: OrderedDict[str, Any] = bind.arguments
            args_f = list(); kwargs_f = dict()
            for pname, argument in arguments.items():
                parameter: inspect.Parameter = parameters[pname]
                annotation: type = parameter.annotation
                argument = cast_impl_(argument, annotation)
                match parameter.kind:
                    case inspect.Parameter.POSITIONAL_ONLY | inspect.Parameter.POSITIONAL_OR_KEYWORD:
                        args_f.append(argument)
                    case inspect.Parameter.VAR_POSITIONAL:
                        args_f.extend(argument)
                    case inspect.Parameter.KEYWORD_ONLY | inspect.Parameter.VAR_KEYWORD:
                        kwargs_f.update({pname: argument})
            result = func(*args_f, **kwargs_f)
            return cast_impl_(result, signature.return_annotation)
        return wrapper_dynamic_cast
    if func_ is None:
        return decorator_dynamic_cast
    else:
        return decorator_dynamic_cast(func_)

@overload
def async_cast(func_: Callable[P, Awaitable[R]], *, strict: bool = ..., cast_impl: Callable[[Any, type], Awaitable[Any]] | None = None)\
    -> Callable[..., Awaitable[R]]: ...

@overload
def async_cast(func_: None = None, *, strict: bool = ..., cast_impl: Callable[[Any, type], Awaitable[Any]] | None = None)\
    -> Callable[[Callable[P, Awaitable[R]]], Callable[..., Awaitable[R]]]: ...

def async_cast(func_: Callable[P, Awaitable[R]] | None = None, *, strict: bool = False, cast_impl: Callable[[Any, type], Awaitable[Any]] | None = None)\
    -> Callable[..., Awaitable[R]] | Callable[[Callable[P, Awaitable[R]]], Callable[..., Awaitable[R]]]:
    if strict: raise NotImplementedError
    async def dynamic_cast_impl_(argument: ARGUMENT, annotation: ANNOTATION) -> Awaitable[ANNOTATION]:
        if isinstance(argument, str) and annotation is int:
            return annotation(float(argument))
        elif annotation in (inspect.Parameter.empty, inspect.Signature.empty):
            return argument
        else:
            return annotation(argument)
    def decorator_async_cast(func: Callable[P, Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        async def wrapper_async_cast(*args: Any, **kwargs: Any) -> R:
            cast_impl_ = cast_impl or dynamic_cast_impl_
            signature: inspect.Signature = inspect.signature(func)
            parameters: MappingProxyType[str, inspect.Parameter] = signature.parameters
            bind: inspect.BoundArguments = signature.bind(*args, **kwargs)
            arguments: OrderedDict[str, Any] = bind.arguments
            args_f = list(); kwargs_f = dict()
            for pname, argument in arguments.items():
                parameter: inspect.Parameter = parameters[pname]
                annotation: type = parameter.annotation
                argument = await cast_impl_(argument, annotation)
                match parameter.kind:
                    case inspect.Parameter.POSITIONAL_ONLY | inspect.Parameter.POSITIONAL_OR_KEYWORD:
                        args_f.append(argument)
                    case inspect.Parameter.VAR_POSITIONAL:
                        args_f.extend(argument)
                    case inspect.Parameter.KEYWORD_ONLY | inspect.Parameter.VAR_KEYWORD:
                        kwargs_f.update({pname: argument})
            return await cast_impl_(await func(*args_f, **kwargs_f), signature.return_annotation)
        return wrapper_async_cast
    if func_ is None:
        return decorator_async_cast
    else:
        return decorator_async_cast(func_)
