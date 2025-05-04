import zlib
from typing import Any

from app.utils.find_git_repo import get_current_git_repo
from app.utils.git_object import read_object


def git_cat_file(args: dict[str, Any]):
    git_repo = get_current_git_repo()
    object_hash = args["object"]
    print_content = args["cat_print_option"]

    object_type, object_length, object_content = read_object(object_hash, git_repo)

    match print_content:
        case "p":
            output = object_content
        case "t":
            output = object_type
        case "s":
            output = object_length
        case _:
            raise ValueError("")

    output = output.decode('utf-8')

    print(output, end="")
