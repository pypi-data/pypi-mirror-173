
import sys as _sys
from typing import List, Callable
from builtins import dict as _dict
from builtins import list as _list
import dataclasses as _dc


@_dc.dataclass(frozen=False,order=True)
class _SystemArg:

    index: int = _dc.field(init=True,default=0)
    arg: str = _dc.field(init=True,default="")
    type: str = _dc.field(init=True,default="")
    name: str = _dc.field(init=True,default="")
    value: str = _dc.field(init=True,default="")

@_dc.dataclass(frozen=False,order=True)
class _LazyData:

    value: (dict[str, _dict] | None) = _dc.field(init=True,default=None)
    is_initialized: bool = _dc.field(init=True,default=False)

    def getvalue(self, fetch: Callable):
        value = self.value
        if not self.is_initialized:
            value = fetch()
            self.value = value
            self.is_initialized = True
        return value




def __init_systemarg(kwargs: _dict = None, asdict: bool = False):
    kwargs_ = {} if kwargs is None else kwargs
    result = _SystemArg(**kwargs_)
    result.value = result.arg
    if "=" in result.arg:
        nv = result.arg.split("=", 1)
        result.name, result.value = nv[0], nv[1]
    else:
        result.name = result.arg
    if asdict:
        result = _dc.asdict(result)
    return result


def __load_systemargs(args: List[str] = None):

    argv = _sys.argv if args is None else args
    return {
        system_arg["name"]: system_arg
        for system_arg in (
            __init_systemarg(kwargs=_dict(index=index, arg=arg), asdict=True)
            for (index, arg) in enumerate(argv)
        )
        if system_arg["name"]
    }


__system_args_data = _LazyData()


def __init_system_args(args: List[str] = None):
    def fetch():
        return __load_systemargs(args=args)

    result = __system_args_data.getvalue(fetch=fetch)
    assert isinstance(result, _dict), __name__ + f" system args is not dict"
    return result


def __dict():
    return __init_system_args()

def __list():
    result = _list(__dict().values())
    result.sort(key=lambda value:value["index"])
    return result


def dict():
    return __dict()


def list():
    return __list()

def init_system_args(args: List[str] = None):

    return __init_system_args(args=args)

