from app.object import GitObjectReader, GitTag, GitObjectWriter
from app.utils.find_git_repo import get_current_git_repo
from app.utils.refs import create_ref


def git_tag(args):
    repo = get_current_git_repo()

    name = args.get("name", None)
    create_tag_obj = args["a"]
    obj = args["object"]
    message = args.get("message", "")

    if name:
        create_tag(repo, name, obj, message, create_tag_obj=create_tag_obj)


def create_tag(repo, name, ref, message = "", create_tag_obj=False):
    git_reader = GitObjectReader(repo)
    object_hash = git_reader.find_object(ref)
    git_writer = GitObjectWriter(repo)

    if create_tag_obj:
        tag = GitTag()
        tag.kvlm = dict()

        tag.kvlm[b'object'] = object_hash.encode()
        tag.kvlm[b'type'] = b'commit'
        tag.kvlm[b'tag'] = name.encode()
        tag.kvlm[b'tagger'] = "Git from scratch".encode()   # TODO: change that to something useful
        tag.kvlm[tag.parser_serializer.message_key] = message.encode()
        tag_hash = git_writer.write(tag, True)
        create_ref(repo, f"tags/{name}", tag_hash)
    else:
        create_ref(repo, f"tags/{name}", object_hash)
