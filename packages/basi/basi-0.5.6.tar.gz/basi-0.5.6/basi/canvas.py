

from ast import arg
from collections import abc
from typing import TypeVar


from typing_extensions import ParamSpec, Self

from celery.canvas import Signature, chain
from . import shared_task


_P = ParamSpec('_P')
_R = TypeVar('_R')
_T = TypeVar('_T')



def _apply_async(self, *a, **kw):
    return self.apply(*a, **kw)
    


@shared_task(name=f'{__package__}.run_in_worker')
def run_in_worker(func: abc.Callable[_P, _R], *args: _P.args, **kwargs: _P.kwargs) -> _R:
    return func(*args, **kwargs)


@shared_task(name=f'{__package__}.throw', apply_async=_apply_async)
def throw(cls: type[Exception], *args: _P.args, **kwargs: _P.kwargs):
    raise (cls if isinstance(cls, Exception) else cls(*args, **kwargs))


@shared_task(name=f'{__package__}.identity', apply_async=_apply_async)
def identity(obj: _T=None):
    return obj

@Signature.register_type()
class forward_ref(Signature):

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if not kwargs and len(args) < 2:
            return cls(identity, args, kwargs, subtask_type='forward_ref')
        return Signature.__new__(cls, *args, **kwargs)
    
    apply_async = _apply_async



del _apply_async
