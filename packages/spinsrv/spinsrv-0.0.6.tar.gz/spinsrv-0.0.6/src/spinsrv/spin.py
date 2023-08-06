import base64
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse
import hashlib

ZeroTime = datetime(1, 1, 1, 0, 0, tzinfo=timezone.utc)


def SHA256(b: bytes):
    m = hashlib.sha256()
    m.update(b)
    return m.hexdigest()


""" CitizenName is a helper type for a spin CitizenName """
CitizenName = str
""" KeyType is a helper type for a spin KeyType """
KeyType = str
""" KeyName is a helper type for a spin KeyName """
KeyName = str


@dataclass
class Key:
    """
    Key is a helper class for a spin Key.
    """

    type: KeyType = ""
    citizen: CitizenName = ""
    name: KeyName = ""
    data: str = ""
    meta: str = ""
    created_at: datetime = ZeroTime
    expires_at: datetime = ZeroTime

    def from_json(j: dict):
        k = Key()
        k.unmarshal_json(j)
        return k

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = KeyType(j["Type"])
        if "Citizen" in j:
            self.citizen = CitizenName(j["Citizen"])
        if "Name" in j:
            self.name = KeyName(j["Name"])
        if "Data" in j:
            self.data = j["Data"]
        if "Meta" in j:
            self.meta = j["Meta"]
        if "CreatedAt" in j:
            self.created_at = isoparse(j["CreatedAt"])
        if "ExpiresAt" in j:
            self.expires_at = isoparse(j["ExpiresAt"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Type"] = self.type
        j["Citizen"] = self.citizen
        j["Name"] = self.name
        j["Data"] = self.data
        j["Meta"] = self.meta
        j["CreatedAt"] = self.created_at.isoformat()
        j["ExpiresAt"] = self.expires_at.isoformat()


@dataclass
class PrivateKey:
    key: Key = Key()
    private: str = ""

    def from_json(j: dict):
        k = PrivateKey()
        k.unmarshal_json(j)
        return k

    def unmarshal_json(self, j: dict):
        self.key.unmarshal_json(j)
        if "Private" in j:
            self.private = j["Private"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Key"] = self.key.to_json()
        j["Private"] = self.private
        return j


@dataclass
class KeyWhichRequest:
    public: str = ""
    private: str = ""

    def from_json(j: dict):
        r = KeyWhichRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        return j


@dataclass
class KeyWhichResponse:
    key: Key = None
    error: str = ""

    def from_json(j: dict):
        r = KeyWhichResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Key" in j:
            self.key = Key.from_json(j["Key"])
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Key"] = self.key.to_json()
        j["Private"] = self.private
        return j


@dataclass
class KeyTempRequest:
    public: str = ""
    private: str = ""
    duration: int = 0  # nanoseconds

    def from_json(j: dict):
        r = KeyTempRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Duration" in j:
            self.duration = j["Duration"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Duration"] = self.duration
        return j


@dataclass
class KeyTempResponse:
    key: Key = None
    private: str = ""
    error: str = ""

    def from_json(j: dict):
        r = KeyTempResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Key" in j:
            self.key = Key.from_json(j["Key"])
        if "Private" in j:
            self.private = j["Private"]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Key"] = self.key.to_json()
        j["Private"] = self.private
        j["Duration"] = self.duration
        return j


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

    def from_json(j: dict):
        r = DirBlock()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Ref" in j:
            self.ref = Ref(j["Ref"])
        if "Offset" in j:
            self.offset = j["Offset"]
        if "Size" in j:
            self.size = j["Size"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Ref"] = self.ref
        j["Offset"] = self.offset
        j["Size"] = self.size
        return j


@dataclass
class DirEntry:
    type: DirEntryType = EntryMissing
    blocks: list[DirBlock] = field(default_factory=list)
    citizen: str = ""
    path: Path = ""
    time: datetime = ZeroTime
    sequence: int = 0

    def from_json(j: dict):
        r = DirEntry()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = DirEntryType(j["Type"])
        if "Blocks" in j and j["Blocks"] is not None:
            self.blocks = [DirBlock.from_json(d) for d in j["Blocks"]]
        if "Citizen" in j:
            self.citizen = j["Citizen"]
        if "Path" in j:
            self.path = j["Path"]
        if "Time" in j:
            self.time = isoparse(j["Time"])
        if "Sequence" in j:
            self.sequence = j["Sequence"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Type"] = self.type
        j["Blocks"] = [b.to_json() for b in self.blocks]
        j["Citizen"] = self.citizen
        j["Path"] = self.path
        j["Time"] = self.time.isoformat()
        j["Sequence"] = self.sequence
        return j


DirOperation = str

MissingDirOperation = ""
PutDirOperation = "put"
DelDirOperation = "del"


@dataclass
class DirOp:
    operation: DirOperation = DirOperation()
    dir_entry: DirEntry = DirEntry()  # embedded

    def from_json(j: dict):
        r = DirOp()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Operation" in j:
            self.operation = DirOperation(j["Operation"])
        # if "DirEntry" in j:
        #     self.dir_entry = DirEntry.from_json(j["DirEntry"])
        # else:
        self.dir_entry = DirEntry.from_json(j)

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Operation"] = self.operation
        self.dir_entry.marshal_json(j)
        return j


BitOperation = str

MissingBitOperation = ""
DelBitOperation = "del"
GetBitOperation = "get"
PutBitOperation = "put"


@dataclass
class BitOp:
    operation: BitOperation = BitOperation()
    ref: Ref = ""
    bytes: bytes = None

    def from_json(j: dict):
        r = BitOp()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Operation" in j:
            self.type = BitOperation(j["Operation"])
        if "Ref" in j:
            self.ref = Ref(j["Ref"])
        if "Bytes" in j:
            self.bytes = base64.b64decode(j["Bytes"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Operation"] = self.operation
        j["Ref"] = self.ref
        j["Bytes"] = base64.b64encode(self.bytes).decode()
        return j


@dataclass
class RefData:
    ref: Ref = ""
    volatile: bool = False
    duration: int = 0

    def from_json(j: dict):
        r = BitOp()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Ref" in j:
            self.ref = Ref(j["Ref"])
        if "Volatile" in j:
            self.ref = Ref(j["Volatile"])
        if "Duration" in j:
            self.duration = j["Duration"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Ref"] = self.ref
        j["Volatile"] = self.volatile
        j["Duration"] = self.duration
        return j


@dataclass
class BitApplyRequest:
    public: str = ""
    private: str = ""
    ops: list[BitOp] = field(default_factory=list)

    def from_json(j: dict):
        r = BitApplyRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = Ref(j["Public"])
        if "Private" in j:
            self.private = Ref(j["Private"])
        if "Ops" in j and j["Ops"] is not None:
            self.ops = [BitOp.from_json(o) for o in j["Ops"]]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Ops"] = [o.to_json() for o in self.ops]
        return j


@dataclass
class BitApplyOutcome:
    ref_data: RefData = RefData()
    bytes: bytearray = None
    Error: str = ""


@dataclass
class BitApplyResponse:
    outcomes: list[BitApplyOutcome] = field(default_factory=list)
    error: str = ""

    def from_json(j: dict):
        r = BitApplyResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Outcomes" in j and j["Outcomes"] is not None:
            self.entries = [BitApplyOutcome.from_json(e) for e in j["Outcomes"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Outcomes"] = [o.to_json() for o in self.outcomes]
        j["Error"] = self.error
        return j


@dataclass
class DirApplyRequest:
    public: str = ""
    private: str = ""
    ops: list[DirOp] = field(default_factory=list)

    def from_json(j: dict):
        r = DirApplyRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = Ref(j["Public"])
        if "Private" in j:
            self.private = Ref(j["Private"])
        if "Ops" in j and j["Ops"] is not None:
            self.ops = [DirOp.from_json(o) for o in j["Ops"]]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Ops"] = [o.to_json() for o in self.ops]
        return j


@dataclass
class DirApplyResponse:
    entries: list[DirEntry] = field(default_factory=list)
    error: str = ""

    def from_json(j: dict):
        r = DirApplyResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entries" in j and j["Entries"] is not None:
            self.entries = [DirEntry.from_json(e) for e in j["Entries"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Entries"] = [e.to_json() for e in self.entries]
        j["Error"] = self.error
        return j


@dataclass
class DirLookupRequest:
    public: str = ""
    private: str = ""
    citizen: CitizenName = ""
    path: Path = ""

    def from_json(j: dict):
        r = DirLookupRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = Ref(j["Public"])
        if "Private" in j:
            self.private = Ref(j["Private"])
        if "Citizen" in j:
            self.citizen = CitizenName(j["CitizenName"])
        if "Path" in j:
            self.path = Path(j["Path"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Citizen"] = self.citizen
        j["Path"] = self.path
        return j


@dataclass
class DirLookupResponse:
    entry: DirEntry = None
    error: str = ""

    def from_json(j: dict):
        r = DirLookupResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entry" in j:
            self.entry = DirEntry.from_json(j["Entry"])
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Entry"] = self.entry.to_json()
        j["Error"] = self.error
        return j


@dataclass
class DirTreeRequest:
    public: str = ""
    private: str = ""
    citizen: CitizenName = ""
    path: Path = ""
    level: int = 0

    def from_json(j: dict):
        r = DirTreeRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = Ref(j["Public"])
        if "Private" in j:
            self.private = Ref(j["Private"])
        if "Citizen" in j:
            self.citizen = CitizenName(j["CitizenName"])
        if "Path" in j:
            self.path = Path(j["Path"])
        if "Level" in j:
            self.level = j["Level"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Citizen"] = self.citizen
        j["Path"] = self.path
        j["Level"] = self.level
        return j


@dataclass
class DirTreeResponse:
    entries: list[DirEntry] = field(default_factory=list)
    error: str = ""

    def from_json(j: dict):
        r = DirTreeResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entries" in j and j["Entries"] is not None:
            self.entries = [DirEntry.from_json(d) for d in j["Entries"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Entries"] = [e.to_json() for e in self.entries]
        j["Error"] = self.error
        return j
