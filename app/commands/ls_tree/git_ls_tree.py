import os
import zlib
from hashlib import sha1

from app.object import GitObjectReader, GitTree, GitTreeLeaf
from app.utils.find_git_repo import get_current_git_repo


class TreeOutputPrinter:
    def __init__(self, names_only=False):
        self.names_only = names_only

    def print(self, item, file_type, prefix=""):
        if self.names_only:
            print(f"{os.path.join(prefix, item.path)}")
        else:
            print(f"{item.mode.decode('utf-8').zfill(6)} {file_type} {item.sha}\t{os.path.join(prefix, item.path)}")


def ls_tree(git_repo, tree_printer, object_hash, git_reader: GitObjectReader, recursive: bool, prefix=""):
    git_object: GitTree = git_reader.read(object_hash)

    for item in git_object.items:
        file_type = item.mode[:2]

        match file_type:
            case b'04':
                file_type = "tree"
            case b'10':
                file_type = "blob"  # A regular file.
            case b'12':
                file_type = "blob"  # A symlink. Blob contents is link target.
            case b'16':
                file_type = "commit"  # A submodule
            case _:
                raise Exception(f"Weird tree leaf mode {item.mode}")

        if not recursive or not file_type == "tree":
            tree_printer.print(item, file_type, prefix)
        else:
            ls_tree(git_repo, tree_printer, item.sha, git_reader, recursive, os.path.join(prefix, item.path))


def git_ls_tree(args):
    git_repo = get_current_git_repo()

    object_hash = args['object']
    name_only = args['name_only']
    recursive = args['recursive']

    git_reader = GitObjectReader(git_repo)
    tree_printer = TreeOutputPrinter(name_only)

    ls_tree(git_repo, tree_printer, object_hash, git_reader, recursive=recursive)

