import argparse


def ls_tree_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name-only', action='store_true')
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('object')

    return parser
