import os
from pathlib import Path
import re


def is_git_directory(path: str | Path):
    c_path = Path(path)
    objects_dir = c_path.joinpath('objects')
    refs_dir = c_path.joinpath('refs')
    head_file = c_path.joinpath('HEAD')

    if head_file.exists() and objects_dir.exists() and refs_dir.exists():
        return True

    return False


def find_git_repo(path: str | Path):
    c_path = Path(path)
    git_dir = [c_dir for c_dir in c_path.iterdir() if c_dir.is_dir() and c_dir.name.startswith('.') and is_git_directory(c_dir)]
    if len(git_dir) > 0:
        return git_dir[0]
    else:
        if str(c_path.parent) != str(c_path):
            return find_git_repo(c_path.parent)
        else:
            return None



def get_current_git_repo() -> Path:
    repo_path = os.getenv("GIT_DIR")

    if repo_path is None:
        repo_path = find_git_repo(os.getcwd())

    return Path(repo_path)
