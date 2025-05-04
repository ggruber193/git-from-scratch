import argparse


def checkout_parser():
    parser = argparse.ArgumentParser(description='Checkout a git repository.')
    parser.add_argument('commit', help='Commit to checkout.')
    parser.add_argument('path', help='Empty directory to checkout on.')
    return parser
