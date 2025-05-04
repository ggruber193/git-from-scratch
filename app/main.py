import sys
import os
import logging
import argparse

from app.commands.cat_file.parser import cat_file_parser
from app.commands.init.git_init import git_init
from app.commands.cat_file.git_cat_file import git_cat_file

def main():
    parser = argparse.ArgumentParser(description='Implementation of git from scratch')

    subparsers = parser.add_subparsers(dest="subparser_name")

    parser_init = subparsers.add_parser('init', description="Initialize new git repository")
    parser_cat_file = subparsers.add_parser('cat-file', parents=[cat_file_parser()], add_help=False, description="Read blobs")

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
