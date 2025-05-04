import sys
import os
import logging
import argparse


from app.commands.init.git_init import git_init
from app.commands.cat_file.git_cat_file import git_cat_file

def main():
    parser = argparse.ArgumentParser(description='Implementation of git from scratch')

    subparsers = parser.add_subparsers(dest="subparser_name")

    parser_init = subparsers.add_parser('init', description="Initialize new git repository")
    parser_cat_file = subparsers.add_parser('cat-file', description="Read blobs")
    cat_file_view_options = parser_cat_file.add_mutually_exclusive_group(required=True)

    cat_file_view_options.add_argument('-p', help="pretty-print object's content", action="store_true")
    cat_file_view_options.add_argument('-t', help="pretty-print object's type", action="store_true")
    cat_file_view_options.add_argument('-s', help="pretty-print object's size", action="store_true")

    parser_cat_file.add_argument('object', help="blob hash")

    args = parser.parse_args()
    subcommand = args.subparser_name

    match subcommand:
        case 'init':
            git_init()
        case 'cat-file':
            git_cat_file(args.__dict__)
        case _:
            raise ValueError(f"Invalid subcommand: {subcommand}.")


if __name__ == "__main__":
    main()
