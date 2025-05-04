import zlib
from hashlib import sha1

from app.utils.find_git_repo import get_current_git_repo
from app.utils.git_object import create_object, calculate_object_hash, write_object


def git_hash_object(args):
    git_repo = get_current_git_repo()

    file_to_hash = args['file']
    object_type = args['type']
    write_to_database = args['w']

    with open(file_to_hash, 'r') as f:
        file_content = f.read()

    file_length = len(file_content)

    _object = create_object(object_type, file_length, file_content)
    object_hash = calculate_object_hash(_object)

    if write_to_database:
        write_object(_object, object_hash, git_repo)

    print(object_hash)
