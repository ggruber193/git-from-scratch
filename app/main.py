import sys
import os
import logging
import argparse


from app.commands.init.git_init import git_init

def main():
    parser = argparse.ArgumentParser(description='Implementation of git from scratch')

    subparsers = parser.add_subparsers(dest="subparser_name")

    parser_init = subparsers.add_parser('init', description="Initialize new git repository")

    args = parser.parse_args()
    subcommand = args.subparser_name

    match subcommand:
        case 'init':
            git_init()
        case _:
            raise ValueError(f"Invalid subcommand: {subcommand}.")


if __name__ == "__main__":
    main()
