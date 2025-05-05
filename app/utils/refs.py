from pathlib import Path

from app.utils.find_git_repo import get_current_git_repo


def find_file(start_path, path):
    queue = [start_path]
    while queue:
        c_path = queue.pop(0)
        for file in c_path.iterdir():
            if file.is_file() and str(path) in str(file):
                return file
            elif file.is_dir():
                queue.append(file)
    return None


def ref_resolve(repo: str | Path, ref):
    repo = Path(repo)
    refs_path = Path(repo).joinpath(ref)

    while True:
        with open(refs_path) as f:
            data = f.read()[:-1]
        if data.startswith('ref: '):
            refs_path = repo.joinpath(data[5:])
        else:
            output = data
            break
    return output


def ref_list(repo, path=None):
    # TODO: implementation not finished
    if not path:
        path = Path(repo).joinpath('refs')
    else:
        path = Path(path)
    ret = dict()
    for f in path.iterdir():
        pass


def create_ref(repo, path, tag_hash):
    full_path = Path(repo).joinpath("refs").joinpath(path)
    with open(full_path, 'w') as f:
        f.write(tag_hash+'\n')




if __name__ == '__main__':
    repo = get_current_git_repo()
    ref = "refs/remotes/origin/HEAD"

    print(ref_resolve(repo, ref))
