import argparse


def cat_file_parser():
    parser = argparse.ArgumentParser()
    cat_file_view_options = parser.add_mutually_exclusive_group(required=True)

    cat_file_view_options.add_argument('-p', help="pretty-print object's content", action="store_const",
                                       dest="cat_print_option", const="p")
    cat_file_view_options.add_argument('-t', help="pretty-print object's type", action="store_const",
                                       dest="cat_print_option", const="t")
    cat_file_view_options.add_argument('-s', help="pretty-print object's size", action="store_const",
                                       dest="cat_print_option", const="s")

    parser.add_argument('object', help="blob hash")
    return parser
