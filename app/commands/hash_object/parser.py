import argparse


def hash_object_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', help="Specify the type", default='blob')
    parser.add_argument('-w', help="Write the object into the database", action='store_true')
    parser.add_argument('file', help="The file to hash")

    return parser
