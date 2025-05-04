from pathlib import Path

from app.object import GitObjectReader, GitObjectTypes
from app.utils.find_git_repo import get_current_git_repo


def git_checkout(args):
    repo = get_current_git_repo()

    commit = args["commit"]
    path = Path(args["path"])

    if path.exists() and len(list(path.iterdir())) > 0:
        raise FileExistsError("Directory '{}' already exists and is not empty.".format(path))

    path.mkdir(parents=True, exist_ok=True)

    git_reader = GitObjectReader(repo)

    git_object = git_reader.read(commit)

    if git_object.object_type == GitObjectTypes.commit:
        git_object = git_reader.read(git_object.kvlm[b"tree"].decode())

    tree_checkout(git_reader, git_object, path)


def tree_checkout(git_reader: GitObjectReader, tree, path: Path):
    for item in tree.items:
        obj = git_reader.read(item.sha)
        dest = path.joinpath(item.path)

        if obj.object_type == GitObjectTypes.tree:
            dest.mkdir(parents=True, exist_ok=True)
            tree_checkout(git_reader, obj, dest)
        elif obj.object_type == GitObjectTypes.blob:
            with open(dest, "wb") as f:
                f.write(obj.data)
