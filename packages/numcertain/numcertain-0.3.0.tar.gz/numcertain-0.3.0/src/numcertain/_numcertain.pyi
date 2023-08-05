from typing import Literal, Protocol, overload

from numpy._typing._ufunc import _UFunc_Nin1_Nout1

nominal: _UFunc_Nin1_Nout1[Literal["nominal"], Literal[1], None]
uncertainty: _UFunc_Nin1_Nout1[Literal["uncertainty"], Literal[1], None]

class _UncertainOp(Protocol):
    @overload
    def __call__(self, other: bool, /) -> uncertain: ...
    @overload
    def __call__(self, other: int, /) -> uncertain: ...
    @overload
    def __call__(self, other: float, /) -> uncertain: ...
    @overload
    def __call__(self, other: uncertain, /) -> uncertain: ...

class uncertain:
    def __init__(self, nominal, uncertainity) -> None: ...
    __add__: _UncertainOp
    __radd__: _UncertainOp
    __sub__: _UncertainOp
    __rsub__: _UncertainOp
    __mul__: _UncertainOp
    __rmul__: _UncertainOp
    __truediv__: _UncertainOp
    __rtruediv__: _UncertainOp
    nominal: float
    uncertainty: float
