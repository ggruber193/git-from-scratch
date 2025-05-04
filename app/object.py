import zlib
from abc import abstractmethod, ABC
from enum import Enum
from hashlib import sha1
from pathlib import Path
import re

from app.utils.find_git_repo import get_current_git_repo
from app.utils.parsing import KeyValueParser
from app.utils.refs import ref_resolve


class GitObjectTypes(Enum):
    tree = "tree"
    commit = "commit"
    tag = "tag"
    blob = "blob"

class GitObject(ABC):
    @property
    @abstractmethod
    def object_type(self) -> GitObjectTypes:
        pass
    def __init__(self, data=None):
        if data is not None:
            self.deserialize(data)
        else:
            self.init()

    @abstractmethod
    def deserialize(self, data):
        pass

    def init(self):
        pass

    @abstractmethod
    def serialize(self):
        pass


class GitBlob(GitObject):
    object_type = GitObjectTypes.blob

    def serialize(self):
        return self.data

    def deserialize(self, data):
        self.data = data

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, "r") as f:
            data = f.read().encode("utf-8")
        return cls(data)


class GitCommit(GitObject):
    object_type = GitObjectTypes.commit

    def deserialize(self, data):
        self.kvlm = self.parser_serializer.parse_key_value_list_with_message(data)

    def serialize(self):
        return self.parser_serializer.serialize_parse_key_value_list_with_message(self.kvlm)

    def init(self):
        self.kvlm = dict()
        self.parser_serializer = KeyValueParser()

class GitTreeLeaf:
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mode}, {self.path}, {self.sha})"

class GitTree(GitObject):
    object_type = GitObjectTypes.tree

    def serialize(self):
        return self._tree_serialize(self)

    def deserialize(self, data):
        self.items = self._tree_parse(data)

    def init(self):
        self.items = []


    @staticmethod
    def _tree_parse(data):
        leaves = []
        while data:
            parts = data.split(b'\x00', maxsplit=1)

            mode = parts[0].split(b' ')[0]
            if len(mode) == 5:
                mode = mode.zfill(6)
            filename = parts[0].split(b' ')[1].decode('utf-8')
            sha_hash = parts[1][:20].hex()
            leaf = GitTreeLeaf(mode, filename, sha_hash)
            leaves.append(leaf)
            data = parts[1][20:]
        return leaves

    @staticmethod
    def _tree_serialize(obj: u'GitTree'):
        obj.items.sort(key=lambda item: item.path if item.mode.startswith(b'10') else item.path + '/')
        ret = ''.join([f"{i.mode} {i.path}\x00{int(i.sha, 16).to_bytes(20, byteorder='big')}" for i in obj.items]).encode('utf-8')
        return ret


class GitTag(GitCommit):
    object_type = GitObjectTypes.tag


class GitObjectReader:
    def __init__(self, repo: str | Path = None):
        if repo is None:
            self.repo = get_current_git_repo()
        else:
            self.repo = repo

    def _resolve_object(self, name):
        candidates = []
        hashRE = re.compile(r"^[0-9A-Fa-f]{4,40}$")

        if name == 'HEAD':
            return [ref_resolve(self.repo, name)]

        if hashRE.match(name):
            name = name.lower()
            prefix = name[:2]
            path = self.repo.joinpath("objects").joinpath(prefix)
            if path.exists():
                rem = name[2:]
                for file in self.repo.joinpath("objects").joinpath(prefix).iterdir():
                    if file.name.startswith(rem):
                        candidates.append(prefix+file.name)

        as_tag = ref_resolve(self.repo, "refs/tags/" + name)
        if as_tag:
            candidates.append(as_tag)
        as_branch = ref_resolve(self.repo, "refs/heads/" + name)
        if as_branch:
            candidates.append(as_branch)

        return candidates

    def find_object(self, name, fmt=None, follow=True):
        object_hash = self._resolve_object(name)
        if not object_hash:
            raise Exception(f"Can't find object {name}")
        if len(object_hash) > 1:
            raise Exception(f"Ambiguous object {name}")

        object_hash = object_hash[0]
        if not fmt:
            return object_hash

        while True:
            obj = self.read(object_hash)

            if obj.object_type == fmt:
                return object_hash

            if not follow:
                return None

            # Follow tags
            if obj.object_type == 'tag':
                object_hash = obj.kvlm[b'object'].decode("ascii")
            elif obj.object_type == 'commit' and fmt == b'tree':
                object_hash = obj.kvlm[b'tree'].decode("ascii")
            else:
                return None

    def _get_object_path(self, object_hash):
        object_path = f"{object_hash[:2]}/{object_hash[2:]}"
        return self.repo.joinpath("objects").joinpath(object_path)

    def read(self, object_hash: str) -> GitObject:
        object_repo_path = self._get_object_path(object_hash)

        with open(object_repo_path, "rb") as f:
            contents = zlib.decompress(f.read())

        object_content = contents.split(b'\x00', maxsplit=1)[1]
        object_type = contents.split(b' ', maxsplit=1)[0]
        # object_length = contents.split(b' ', maxsplit=1)[1].split(b'\x00', maxsplit=1)[0]

        match object_type:
            case b"blob":   c=GitBlob
            case b"tree":   c=GitTree
            case b"commit": c=GitCommit
            case b"tag":    c=GitTag
            case _: raise Exception(f"Unknown object type: {object_type.decode()} for sha: {object_hash}")

        return c(object_content)

def calculate_object_hash(_object: bytes):
    object_hash = sha1(_object).hexdigest()
    return object_hash

class GitObjectWriter:
    def __init__(self, repo: str | Path = None):
        if repo is None:
            self.repo = Path(get_current_git_repo())
        else:
            self.repo = Path(repo)

    @staticmethod
    def _calculate_object_hash(git_object: bytes):
        return sha1(git_object).hexdigest()

    def _get_object_path(self, object_hash) -> Path:
        object_path = f"{object_hash[:2]}/{object_hash[2:]}"
        return self.repo.joinpath("objects").joinpath(object_path)

    def write(self, git_object: GitObject, write_to_database=False):
        object_serialized = git_object.serialize()
        object_length = len(object_serialized)
        object_type = git_object.object_type.value
        output_object = f"{object_type} {object_length}\x00".encode('utf-8') + object_serialized

        object_hash = self._calculate_object_hash(output_object)

        if write_to_database:
            object_path = self._get_object_path(object_hash)
            object_path.parent.mkdir(parents=True, exist_ok=True)
            with open(object_path, "wb") as f:
                f.write(zlib.compress(output_object))

        return object_hash
