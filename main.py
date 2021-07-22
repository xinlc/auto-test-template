"""
main
"""

__author__ = 'Richard'
__version__ = '2021-07-18'

# main.py
import argparse


def main():
    parser = argparse.ArgumentParser(prog="testing", usage="This is a demo")
    parser.add_argument("--name", default='Richard', help="This is a demo framework", action="store")
    args = parser.parse_args()
    if args.name:
        print("Hello %s" % args.name)


if __name__ == "__main__":
    main()
