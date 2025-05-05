import shutil
import sys
import unittest
from pathlib import Path
from uuid import uuid4

import subprocess

from test.utils import TestArgs, GitTestRepo


class TestGitCatFile(unittest.TestCase):

    def setUp(self):
        self.test_environment_path = Path(f"git_from_scratch_test_repo_{str(uuid4())}")
        self.git_test_repo = GitTestRepo(self.test_environment_path)
        self.git_test_repo.setup()
        self.test_args = TestArgs("cat-file")
        self.test_object = self.git_test_repo.hash_object()


    def test_cat_file_print_content(self):
        git_output = subprocess.check_output(['git', 'cat-file', '-p', str(self.test_object)])
        impl_output = subprocess.check_output(self.test_args.get_cmd(f'-p {str(self.test_object)}'))

        self.assertEqual(git_output, impl_output)

    def test_cat_file_print_length(self):
        git_output = subprocess.check_output(['git', 'cat-file', '-s', str(self.test_object)]).rstrip()
        impl_output = subprocess.check_output(self.test_args.get_cmd(f'-s {str(self.test_object)}'))

        self.assertEqual(git_output, impl_output)

    def test_cat_file_print_type(self):
        git_output = subprocess.check_output(['git', 'cat-file', '-t', str(self.test_object)]).rstrip()
        impl_output = subprocess.check_output(self.test_args.get_cmd(f'-t {str(self.test_object)}'))

        self.assertEqual(git_output, impl_output)

    def test_cat_file_nonexistent_hash(self):
        random_input = "kdsjfkl"

        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.check_call(self.test_args.get_cmd(f'-t {random_input}'), stderr=subprocess.DEVNULL)

        self.assertEqual(context.exception.returncode, 1)

    def tearDown(self):
        self.git_test_repo.destroy()
