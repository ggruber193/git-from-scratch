import argparse


def tag_parser():
    parser=argparse.ArgumentParser()

    parser.add_argument('-a', action="store_true", help="Create tag object")
    parser.add_argument('name', nargs='?', help="Name of the tag")
    parser.add_argument('object', default="HEAD", nargs='?', help="The object the new tag will point to")
