import zlib
from hashlib import sha1

from app.utils.find_git_repo import get_current_git_repo
from app.utils.git_object import find_object, read_object


def git_ls_tree(args):
    git_repo = get_current_git_repo()

    object_hash = args['object']
    name_only = args['name_only']

    object_type, object_length, object_content = read_object(object_hash, git_repo)

    tree_content = object_content
    contents = []
    while tree_content:
        parts = tree_content.split(b'\x00', maxsplit=1)

        mode = parts[0].split(b' ')[0].decode('utf-8')
        filename = parts[0].split(b' ')[1].decode('utf-8')
        sha_hash = parts[1][:20].hex()

        c_type, c_length, c_content = read_object(sha_hash, git_repo)

        entry = (mode, filename, sha_hash, c_type.decode('utf-8'))
        contents.append(entry)

        tree_content = parts[1][20:]

    max_lengths = [max([len(j[i]) for j in contents]) for i in range(len(contents[0]))]

    if name_only:
        output = '\n'.join([i[1] for i in contents])
    else:
        output = '\n'.join([f"{i[0].zfill(max_lengths[0])} {i[3].zfill(max_lengths[3])} {i[2]}    {i[1]}" for i in contents])

    print(output)
