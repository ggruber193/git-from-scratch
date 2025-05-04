import zlib
from typing import Any

from app.object import GitObjectReader
from app.utils.find_git_repo import get_current_git_repo


def git_cat_file(args: dict[str, Any]):
    git_repo = get_current_git_repo()
    object_hash = args["object"]
    print_content = args["cat_print_option"]

    git_reader = GitObjectReader(git_repo)
    git_object = git_reader.read(object_hash)

    match print_content:
        case "p":
            output = git_object.serialize().decode('utf-8')
        case "t":
            output = git_object.object_type.value
        case "s":
            output = len(git_object.serialize())
        case _:
            raise ValueError("")

    print(output, end="")
