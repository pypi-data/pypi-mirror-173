from dataclasses import dataclass, field
from datetime import datetime, timedelta

CitizenName = str
KeyType = str
KeyName = str


@dataclass
class Key:
    type: KeyType = ""
    citizen: CitizenName = ""
    name: KeyName = ""
    data: str = ""
    meta: str = ""
    created_at: datetime = None
    expires_at: datetime = None


@dataclass
class PrivateKey:
    key: Key = Key()
    private: str = ""


@dataclass
class KeyWhichRequest:
    public: str = ""
    private: str = ""


@dataclass
class KeyWhichResponse:
    key: Key = None
    error: str = ""


@dataclass
class KeyTempRequest:
    public: str = ""
    private: str = ""
    duration: int = 0  # nanoseconds


@dataclass
class KeyTempResponse:
    key: Key = None
    private: str = ""
    error: str = ""


Path = str
Ref = str
DirEntryType = str

EntryMissing: DirEntryType = ""
EntryDir: DirEntryType = "dir"
EntryFile: DirEntryType = "file"

SeqNotExist = -1
SeqIgnore = 0
SeqBase = 1
MaxBlockSize = 10 * (1024 * 1024)


@dataclass
class DirBlock:
    ref: Ref = ""
    offset: int = 0
    size: int = 0


@dataclass
class DirEntry:
    type: DirEntryType = EntryMissing
    blocks: list[DirBlock] = field(default_factory=list)
    citizen: str = ""
    path: Path = ""
    time: datetime = None
    sequence: int = 0


DirOperation = str

MissingDirOperation = ""
PutDirOperation = "put"
DelDirOperation = "del"


@dataclass
class DirOp:
    operation: DirOperation = DirOperation()
    dir_entry: DirEntry = DirEntry()


BitOperation = str

MissingBitOperation = ""
DelBitOperation = "del"
GetBitOperation = "get"
PutBitOperation = "put"


@dataclass
class BitOp:
    operation: BitOperation = BitOperation()
    ref: Ref = ""
    bytes: bytearray = None
