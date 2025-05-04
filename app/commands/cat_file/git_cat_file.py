import zlib
from typing import Any

from app.utils import get_current_git_repo

def git_cat_file(args: dict[str, Any]):
    git_repo = get_current_git_repo()
    object_hash = args["object"]
    print_content = args.get("p", False)
    print_type = args.get("t", False)
    print_size = args.get("s", False)

    object_path = f"{object_hash[:2]}/{object_hash[2:]}"
    object_repo_path = git_repo.joinpath("objects").joinpath(object_path)

    with open(object_repo_path, "rb") as f:
        contents = zlib.decompress(f.read())

    if print_content:
        output = contents.split(b'\x00')[1]
    elif print_type:
        output = contents.split(b' ')[0]
    elif print_size:
        output = contents.split(b' ')[1].split(b'\x00')[0]
    else:
        raise ValueError("")

    output = output.decode('utf-8')

    print(output, end="")
