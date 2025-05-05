import shutil
import unittest
from pathlib import Path
from uuid import uuid4

import subprocess

from test.utils import TestArgs, GitTestRepo


class TestGitHashObject(unittest.TestCase):

    def setUp(self):
        self.test_environment_path = Path(f"git_from_scratch_test_repo_{str(uuid4())}").absolute()
        self.git_test_repo = GitTestRepo(self.test_environment_path)
        self.git_test_repo.setup()
        self.test_file = self.git_test_repo.create_file()
        self.test_args = TestArgs("hash-object")

    def test_hash_object_correct_hash(self):
        git_output = subprocess.check_output(['git', 'hash-object', str(self.test_file)]).rstrip()
        impl_output = subprocess.check_output(self.test_args.get_cmd(str(self.test_file))).rstrip()

        self.assertEqual(git_output, impl_output)

    def test_hash_object_correct_object(self):
        git_output = subprocess.check_output(['git', 'hash-object', '-w', str(self.test_file)]).rstrip().decode()
        git_file = self.test_environment_path.joinpath(".git/objects").joinpath(f"{git_output[:2]}/{git_output[2:]}")
        git_file_exists = git_file.exists()
        shutil.move(git_file, 'tmp')

        impl_output = subprocess.check_output(self.test_args.get_cmd(f"-w {str(self.test_file)}")).rstrip().decode()
        impl_file = self.test_environment_path.joinpath(".git/objects").joinpath(f"{impl_output[:2]}/{impl_output[2:]}")
        impl_file_exists = impl_file.exists()

        self.assertEqual(git_file_exists, impl_file_exists)
        self.assertEqual(str(git_file), str(impl_file))

    def tearDown(self):
        self.git_test_repo.destroy()
