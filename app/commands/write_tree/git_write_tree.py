from pathlib import Path

from app.utils.find_git_repo import get_current_git_repo
from app.utils.git_object import create_blob, calculate_object_hash


def iterate_working_dir(path: Path):
    for file in path.iterdir():
        if file.is_dir():
            pass
        if file.is_file():
            _object = create_blob(file)
            object_hash = calculate_object_hash(_object)
            filename = ''



def git_write_tree():
    git_repo = get_current_git_repo()
    working_dir = git_repo.parent


