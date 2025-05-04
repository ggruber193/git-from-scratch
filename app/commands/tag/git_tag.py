from app.object import GitObjectReader, GitTag
from app.utils.find_git_repo import get_current_git_repo


def git_tag(args):
    repo = get_current_git_repo()

    name = args["name"]
    create_tag_obj = args["a"]
    obj = args["object"]


def create_tag(repo, name, ref, create_tag_obj=False):
    # TODO need to implement this
    git_reader = GitObjectReader(repo)
    object_hash = git_reader.find_object(ref)

    if create_tag_obj:
        tag = GitTag()
        tag.kvlm = dict()

