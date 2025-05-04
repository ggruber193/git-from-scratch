import zlib

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
