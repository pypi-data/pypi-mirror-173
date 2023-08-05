import sys
from _typeshed import ReadableBuffer, Self
from collections.abc import Callable, Set as AbstractSet
from typing import Protocol
from typing_extensions import final

if sys.version_info >= (3, 11):
    __all__ = (
        "md5",
        "sha1",
        "sha224",
        "sha256",
        "sha384",
        "sha512",
        "blake2b",
        "blake2s",
        "sha3_224",
        "sha3_256",
        "sha3_384",
        "sha3_512",
        "shake_128",
        "shake_256",
        "new",
        "algorithms_guaranteed",
        "algorithms_available",
        "pbkdf2_hmac",
        "file_digest",
    )
else:
    __all__ = (
        "md5",
        "sha1",
        "sha224",
        "sha256",
        "sha384",
        "sha512",
        "blake2b",
        "blake2s",
        "sha3_224",
        "sha3_256",
        "sha3_384",
        "sha3_512",
        "shake_128",
        "shake_256",
        "new",
        "algorithms_guaranteed",
        "algorithms_available",
        "pbkdf2_hmac",
    )

class _Hash:
    @property
    def digest_size(self) -> int: ...
    @property
    def block_size(self) -> int: ...
    @property
    def name(self) -> str: ...
    def __init__(self, data: ReadableBuffer = ...) -> None: ...
    def copy(self: Self) -> Self: ...
    def digest(self) -> bytes: ...
    def hexdigest(self) -> str: ...
    def update(self, __data: ReadableBuffer) -> None: ...

if sys.version_info >= (3, 9):
    def new(name: str, data: ReadableBuffer = ..., *, usedforsecurity: bool = ...) -> _Hash: ...
    def md5(string: ReadableBuffer = ..., *, usedforsecurity: bool = ...) -> _Hash: ...
    def sha1(string: ReadableBuffer = ..., *, usedforsecurity: bool = ...) -> _Hash: ...
    def sha224(string: ReadableBuffer = ..., *, usedforsecurity: bool = ...) -> _Hash: ...
    def sha256(string: ReadableBuffer = ..., *, usedforsecurity: bool = ...) -> _Hash: ...
    def sha384(string: ReadableBuffer = ..., *, usedforsecurity: bool = ...) -> _Hash: ...
    def sha512(string: ReadableBuffer = ..., *, usedforsecurity: bool = ...) -> _Hash: ...

elif sys.version_info >= (3, 8):
    def new(name: str, data: ReadableBuffer = ...) -> _Hash: ...
    def md5(string: ReadableBuffer = ...) -> _Hash: ...
    def sha1(string: ReadableBuffer = ...) -> _Hash: ...
    def sha224(string: ReadableBuffer = ...) -> _Hash: ...
    def sha256(string: ReadableBuffer = ...) -> _Hash: ...
    def sha384(string: ReadableBuffer = ...) -> _Hash: ...
    def sha512(string: ReadableBuffer = ...) -> _Hash: ...

else:
    def new(name: str, data: ReadableBuffer = ...) -> _Hash: ...
    def md5(__string: ReadableBuffer = ...) -> _Hash: ...
    def sha1(__string: ReadableBuffer = ...) -> _Hash: ...
    def sha224(__string: ReadableBuffer = ...) -> _Hash: ...
    def sha256(__string: ReadableBuffer = ...) -> _Hash: ...
    def sha384(__string: ReadableBuffer = ...) -> _Hash: ...
    def sha512(__string: ReadableBuffer = ...) -> _Hash: ...

algorithms_guaranteed: AbstractSet[str]
algorithms_available: AbstractSet[str]

def pbkdf2_hmac(
    hash_name: str, password: ReadableBuffer, salt: ReadableBuffer, iterations: int, dklen: int | None = ...
) -> bytes: ...

class _VarLenHash:
    digest_size: int
    block_size: int
    name: str
    def __init__(self, data: ReadableBuffer = ...) -> None: ...
    def copy(self) -> _VarLenHash: ...
    def digest(self, __length: int) -> bytes: ...
    def hexdigest(self, __length: int) -> str: ...
    def update(self, __data: ReadableBuffer) -> None: ...

sha3_224 = _Hash
sha3_256 = _Hash
sha3_384 = _Hash
sha3_512 = _Hash
shake_128 = _VarLenHash
shake_256 = _VarLenHash

def scrypt(
    password: ReadableBuffer,
    *,
    salt: ReadableBuffer | None = ...,
    n: int | None = ...,
    r: int | None = ...,
    p: int | None = ...,
    maxmem: int = ...,
    dklen: int = ...,
) -> bytes: ...
@final
class _BlakeHash(_Hash):
    MAX_DIGEST_SIZE: int
    MAX_KEY_SIZE: int
    PERSON_SIZE: int
    SALT_SIZE: int

    if sys.version_info >= (3, 9):
        def __init__(
            self,
            __data: ReadableBuffer = ...,
            *,
            digest_size: int = ...,
            key: ReadableBuffer = ...,
            salt: ReadableBuffer = ...,
            person: ReadableBuffer = ...,
            fanout: int = ...,
            depth: int = ...,
            leaf_size: int = ...,
            node_offset: int = ...,
            node_depth: int = ...,
            inner_size: int = ...,
            last_node: bool = ...,
            usedforsecurity: bool = ...,
        ) -> None: ...
    else:
        def __init__(
            self,
            __data: ReadableBuffer = ...,
            *,
            digest_size: int = ...,
            key: ReadableBuffer = ...,
            salt: ReadableBuffer = ...,
            person: ReadableBuffer = ...,
            fanout: int = ...,
            depth: int = ...,
            leaf_size: int = ...,
            node_offset: int = ...,
            node_depth: int = ...,
            inner_size: int = ...,
            last_node: bool = ...,
        ) -> None: ...

blake2b = _BlakeHash
blake2s = _BlakeHash

if sys.version_info >= (3, 11):
    class _BytesIOLike(Protocol):
        def getbuffer(self) -> ReadableBuffer: ...

    class _FileDigestFileObj(Protocol):
        def readinto(self, __buf: bytearray) -> int: ...
        def readable(self) -> bool: ...

    def file_digest(
        __fileobj: _BytesIOLike | _FileDigestFileObj, __digest: str | Callable[[], _Hash], *, _bufsize: int = ...
    ) -> _Hash: ...
