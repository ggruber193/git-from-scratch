import sys
import os
import logging
import argparse

from app.commands.cat_file.parser import cat_file_parser
from app.commands.checkout.git_checkout import git_checkout
from app.commands.checkout.parser import checkout_parser
from app.commands.hash_object.git_hash_object import git_hash_object
from app.commands.hash_object.parser import hash_object_parser
from app.commands.init.git_init import git_init
from app.commands.cat_file.git_cat_file import git_cat_file
from app.commands.log.git_log import git_log
from app.commands.log.parser import log_parser
from app.commands.ls_tree.git_ls_tree import git_ls_tree
from app.commands.ls_tree.parser import ls_tree_parser
from app.commands.tag.git_tag import git_tag
from app.commands.tag.parser import tag_parser
from app.commands.write_tree.git_write_tree import git_write_tree


def main():
    parser = argparse.ArgumentParser(description='Implementation of git from scratch')

    subparsers = parser.add_subparsers(dest="subparser_name")

    parser_init = subparsers.add_parser('init', description="Initialize new git repository")
    parser_cat_file = subparsers.add_parser('cat-file', parents=[cat_file_parser()], add_help=False, description="Read blobs")
    parser_hash_object = subparsers.add_parser('hash-object', parents=[hash_object_parser()], add_help=False, description="Hash file")
    parser_ls_tree = subparsers.add_parser('ls-tree', parents=[ls_tree_parser()], add_help=False,
                                               description="ls tree")
    parser_write_tree = subparsers.add_parser('write-tree', help="Write tree")
    parser_log = subparsers.add_parser('log', help='Display commit history', parents=[log_parser()], add_help=False)
    parser_checkout = subparsers.add_parser('checkout', help='Git checkout', parents=[checkout_parser()], add_help=False)
    parser_checkout = subparsers.add_parser('tag', help='Git tag', parents=[tag_parser()], add_help=False)

    args = parser.parse_args()
    subcommand = args.subparser_name

    match subcommand:
        case 'init':
            git_init()
        case 'cat-file':
            git_cat_file(args.__dict__)
        case 'hash-object':
            git_hash_object(args.__dict__)
        case 'ls-tree':
            git_ls_tree(args.__dict__)
        case 'write-tree':
            git_write_tree()
        case 'log':
            git_log(args.__dict__)
        case 'checkout':
            git_checkout(args.__dict__)
        case 'tag':
            git_tag(args.__dict__)
        case _:
            raise ValueError(f"Invalid subcommand: {subcommand}.")


if __name__ == "__main__":
    main()
