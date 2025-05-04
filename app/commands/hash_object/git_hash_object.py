import zlib
from hashlib import sha1

from app.utils.find_git_repo import get_current_git_repo


def git_hash_object(args):
    git_repo = get_current_git_repo()

    file_to_hash = args['file']
    object_type = args['type']
    write_to_database = args['w']

    with open(file_to_hash, 'r') as f:
        file_content = f.read()

    file_length = len(file_content)

    object_header = f"{object_type} {file_length}\x00".encode('utf-8')
    object_hash = sha1(object_header + file_content.encode()).hexdigest()

    if write_to_database:
        object_path = f"{object_hash[:2]}/{object_hash[2:]}"
        object_repo_path = git_repo.joinpath("objects").joinpath(object_path)
        object_repo_path.parent.mkdir(parents=True, exist_ok=True)
        with open(object_repo_path, 'wb') as f:
            f.write(zlib.compress(object_header + file_content.encode()))

    print(object_hash)
