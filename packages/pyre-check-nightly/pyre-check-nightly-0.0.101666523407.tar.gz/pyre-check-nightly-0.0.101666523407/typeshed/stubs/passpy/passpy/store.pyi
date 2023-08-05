from _typeshed import StrPath
from collections.abc import Iterator
from re import Match

class Store:
    def __init__(
        self,
        gpg_bin: str = ...,
        git_bin: str = ...,
        store_dir: str = ...,
        use_agent: bool = ...,
        interactive: bool = ...,
        verbose: bool = ...,
    ) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def is_init(self) -> bool: ...
    def init_store(self, gpg_ids: None | str | list[str], path: StrPath | None = ...) -> None: ...
    def init_git(self) -> None: ...
    def git(self, method: str, *args: object, **kwargs: object) -> None: ...
    def get_key(self, path: StrPath | None) -> str | None: ...
    def set_key(self, path: StrPath | None, key_data: str, force: bool = ...) -> None: ...
    def remove_path(self, path: StrPath, recursive: bool = ..., force: bool = ...) -> None: ...
    def gen_key(
        self, path: StrPath | None, length: int, symbols: bool = ..., force: bool = ..., inplace: bool = ...
    ) -> str | None: ...
    def copy_path(self, old_path: StrPath, new_path: StrPath, force: bool = ...) -> None: ...
    def move_path(self, old_path: StrPath, new_path: StrPath, force: bool = ...) -> None: ...
    def list_dir(self, path: StrPath) -> tuple[list[str], list[str]]: ...
    def iter_dir(self, path: StrPath) -> Iterator[str]: ...
    def find(self, names: None | str | list[str]) -> list[str]: ...
    def search(self, term: str) -> dict[str, list[tuple[str, Match[str]]]]: ...
