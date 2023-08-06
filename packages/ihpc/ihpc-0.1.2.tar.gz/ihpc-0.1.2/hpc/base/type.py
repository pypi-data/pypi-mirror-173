__all__ = ['AnyPosixPath', 'Path', 'Row', 'Std', 'Table']


import pathlib as p
import typing as t

if t.TYPE_CHECKING:
    from .core import RemotePath


AnyPosixPath = t.Union[p.Path, 'RemotePath']
Path = t.Union[str, p.Path]


class Std(t.NamedTuple):
    out: bytes
    err: bytes


class Row:
    def __class_getitem__(cls, T: type) -> type:
        return t.Dict[str, T]


class Table:
    def __class_getitem__(cls, T: type) -> type:
        return t.List[Row[T]]
