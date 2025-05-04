import argparse


def log_parser():
    parser = argparse.ArgumentParser(description='Log parser')
    parser.add_argument('commit', default="HEAD", nargs='?', help='Commit to start at.')

    return parser
