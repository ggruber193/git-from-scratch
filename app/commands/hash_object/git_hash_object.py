import zlib
from hashlib import sha1

from app.object import GitObjectWriter, GitBlob
from app.utils.find_git_repo import get_current_git_repo


def git_hash_object(args):
    git_repo = get_current_git_repo()

    file_to_hash = args['file']
    object_type = args['type']
    write_to_database = args['w']

    git_blob = GitBlob.from_file(file_to_hash)

    git_writer = GitObjectWriter(git_repo)
    object_hash = git_writer.write(git_blob, write_to_database=write_to_database)

    print(object_hash)
