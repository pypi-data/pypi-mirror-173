import types
from _typeshed import StrPath
from os import PathLike
from types import TracebackType
from typing import IO, Any, Protocol

from _imp import (
    acquire_lock as acquire_lock,
    create_dynamic as create_dynamic,
    get_frozen_object as get_frozen_object,
    init_frozen as init_frozen,
    is_builtin as is_builtin,
    is_frozen as is_frozen,
    is_frozen_package as is_frozen_package,
    lock_held as lock_held,
    release_lock as release_lock,
)

SEARCH_ERROR: int
PY_SOURCE: int
PY_COMPILED: int
C_EXTENSION: int
PY_RESOURCE: int
PKG_DIRECTORY: int
C_BUILTIN: int
PY_FROZEN: int
PY_CODERESOURCE: int
IMP_HOOK: int

def new_module(name: str) -> types.ModuleType: ...
def get_magic() -> bytes: ...
def get_tag() -> str: ...
def cache_from_source(path: StrPath, debug_override: bool | None = ...) -> str: ...
def source_from_cache(path: StrPath) -> str: ...
def get_suffixes() -> list[tuple[str, str, int]]: ...

class NullImporter:
    def __init__(self, path: StrPath) -> None: ...
    def find_module(self, fullname: Any) -> None: ...

# Technically, a text file has to support a slightly different set of operations than a binary file,
# but we ignore that here.
class _FileLike(Protocol):
    closed: bool
    mode: str
    def read(self) -> str | bytes: ...
    def close(self) -> Any: ...
    def __enter__(self) -> Any: ...
    def __exit__(self, typ: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None) -> Any: ...

# PathLike doesn't work for the pathname argument here
def load_source(name: str, pathname: str, file: _FileLike | None = ...) -> types.ModuleType: ...
def load_compiled(name: str, pathname: str, file: _FileLike | None = ...) -> types.ModuleType: ...
def load_package(name: str, path: StrPath) -> types.ModuleType: ...
def load_module(name: str, file: _FileLike | None, filename: str, details: tuple[str, str, int]) -> types.ModuleType: ...

# IO[Any] is a TextIOWrapper if name is a .py file, and a FileIO otherwise.
def find_module(
    name: str, path: None | list[str] | list[PathLike[str]] | list[StrPath] = ...
) -> tuple[IO[Any], str, tuple[str, str, int]]: ...
def reload(module: types.ModuleType) -> types.ModuleType: ...
def init_builtin(name: str) -> types.ModuleType | None: ...
def load_dynamic(name: str, path: str, file: Any = ...) -> types.ModuleType: ...  # file argument is ignored
