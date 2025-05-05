import os
import shutil
import stat
import subprocess
from pathlib import Path


class TestArgs:
    def __init__(self, command):
        self.command = command
    def get_cmd(self, parameters: str):
        from app import main
        return ['python', main.__file__, self.command] + [i for i in parameters.split(' ') if i]


class GitTestRepo:
    def __init__(self, path):
        self._cwd = os.getcwd()
        self.path = Path(path)
        self._git_path = self.path.joinpath('.git')
        self.object_path = self._git_path.joinpath('objects')

    def setup(self):
        self.path.mkdir(parents=True, exist_ok=True)
        os.chdir(self.path)
        subprocess.check_call(['git', 'init'], stdout=subprocess.DEVNULL)

    def create_file(self, path="test", content="test content"):
        with open(path, 'w') as f:
            f.write(content)
        return path

    def hash_object(self, path="test", content="test content"):
        file_path = self.create_file(path=path, content=content)
        object_hash = subprocess.check_output(['git', 'hash-object', '-w', str(file_path)]).rstrip().decode()
        return object_hash.rstrip()

    def destroy(self):
        os.chdir(self._cwd)
        destroy_directory(self.path)


def destroy_directory(path):
    for file in path.rglob("*"):
        os.chmod(file, stat.S_IWRITE)
    os.chmod(path, stat.S_IWRITE)
    shutil.rmtree(path)

def setup_git_repo(path: str | Path):
    path.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(['git', 'init', str(path)], )#stdout=subprocess.DEVNULL)
