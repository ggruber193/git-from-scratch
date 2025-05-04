import zlib
from typing import Any

from app.utils.find_git_repo import get_current_git_repo

def git_cat_file(args: dict[str, Any]):
    git_repo = get_current_git_repo()
    object_hash = args["object"]
    print_content = args["cat_print_option"]

    object_path = f"{object_hash[:2]}/{object_hash[2:]}"
    object_repo_path = git_repo.joinpath("objects").joinpath(object_path)

    with open(object_repo_path, "rb") as f:
        contents = zlib.decompress(f.read())

    match print_content:
        case "p":
            output = contents.split(b'\x00')[1]
        case "t":
            output = contents.split(b' ')[0]
        case "s":
            output = contents.split(b' ')[1].split(b'\x00')[0]
        case _:
            raise ValueError("")

    output = output.decode('utf-8')

    print(output, end="")
