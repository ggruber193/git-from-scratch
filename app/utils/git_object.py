import zlib
from hashlib import sha1
from pathlib import Path

from app.utils.find_git_repo import get_current_git_repo


def find_object(object_hash, git_repo=None):
    if git_repo is None:
        git_repo = get_current_git_repo()
    object_path = f"{object_hash[:2]}/{object_hash[2:]}"
    return git_repo.joinpath("objects", object_path)


def read_object(object_path, git_repo=None):
    object_repo_path = find_object(object_path, git_repo)

    with open(object_repo_path, "rb") as f:
        contents = zlib.decompress(f.read())

    object_content = contents.split(b'\x00', maxsplit=1)[1]
    object_type = contents.split(b' ', maxsplit=1)[0]
    object_length = contents.split(b' ', maxsplit=1)[1].split(b'\x00', maxsplit=1)[0]

    return object_type, object_length, object_content


def create_blob(file_path: str | Path):
    object_type = "blob"
    with open(file_path, "r") as f:
        contents = f.read()
    object_length = len(contents)
    return create_object(object_type, object_length, contents)


def create_object(object_type, object_length, object_content):
    object_header = f"{object_type} {object_length}\x00".encode('utf-8')
    object_content = object_content.encode('utf-8')
    return object_header + object_content

def calculate_object_hash(_object: bytes):
    object_hash = sha1(_object).hexdigest()
    return object_hash

def write_object(_object, object_hash, git_repo=None):
    if git_repo is None:
        git_repo = get_current_git_repo()

    object_path = f"{object_hash[:2]}/{object_hash[2:]}"
    object_repo_path = git_repo.joinpath("objects").joinpath(object_path)
    object_repo_path.parent.mkdir(parents=True, exist_ok=True)
    with open(object_repo_path, 'wb') as f:
        f.write(zlib.compress(_object))
