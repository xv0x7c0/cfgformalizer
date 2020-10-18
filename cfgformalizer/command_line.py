import argparse
import hashlib
import re
import sys

from cfgformalizer.cisco.cisco import Cisco


class RegexpAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        regexp = re.compile(value)
        items = getattr(namespace, self.dest, None)
        if items is None:
            items = []
        if option_string == "--include":
            items.append(("include", regexp))
        if option_string == "--exclude":
            items.append(("exclude", regexp))
        setattr(namespace, self.dest, items)


class ReplacementAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        regexp = re.compile(values[0])
        items = getattr(namespace, self.dest, None)
        if items is None:
            items = []
        items.append((regexp, values[1]))
        setattr(namespace, self.dest, items)


def get_parser():
    """Return CLI parser"""
    description = "Expand context of Cisco configuration file to make them greppable"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "--linenum",
        dest="linenum",
        help="Display original config line numbers",
        action="store_true",
    )

    parser.add_argument(
        "--seqnum",
        dest="seqnum",
        help="Display stanza sequence number",
        action="store_true",
    )

    parser.add_argument(
        "--comments", dest="comments", help="Display comments", action="store_true"
    )

    parser.add_argument(
        "--sort",
        dest="sort",
        help="Sort statements alphabetically",
        action="store_true",
    )

    parser.add_argument(
        "--delimiter",
        dest="delimiter",
        default=" ",
        help="Change context delimiter (space by default)",
        action="store",
    )

    parser.add_argument(
        "--include",
        dest="regexps",
        help="Stack regexps for filtering output",
        action=RegexpAction,
    )

    parser.add_argument(
        "--exclude",
        dest="regexps",
        help="Stack regexps for filtering output",
        action=RegexpAction,
    )

    parser.add_argument(
        "--normal",
        dest="normal",
        help="Display normal config style instead of formal",
        action="store_true",
    )

    parser.add_argument(
        "--replace",
        nargs=2,
        dest="replace",
        metavar=("REGEXP", "STRING"),
        help="Replace regexp with string",
        action=ReplacementAction,
    )

    parser.add_argument(
        "--hash",
        dest="hash",
        help="Hash stanza for easy comparison",
        action="store_true",
    )

    parser.add_argument(
        "--hash-algorithm",
        dest="hash_algo",
        help="Hash algorithm used for hashing",
        action="store",
        default="sha256",
    )

    parser.add_argument("files", nargs="+", metavar="FILE", help="Configuration file")
    return parser


def build_stanza(config, regexps=None, comments=False, sort=False):
    s = Cisco.parse(config)
    if regexps:
        for regexp_type, regexp in regexps:
            if regexp_type == "include":
                s = s.like(regexp)
            elif regexp_type == "exclude":
                s = s.unlike(regexp)
    if not comments:
        s = s.without_comments()
    if sort:
        s = s.sort()
    return s


def stringify_stanza(stanza, normal=False, linenum=False, seqnum=False, delimiter=" "):
    if normal:
        return stanza.normal(linenum=linenum, seqnum=seqnum, delimiter=delimiter)
    else:
        return stanza.formal(linenum=linenum, seqnum=seqnum, delimiter=delimiter)


def replace_pattern(string, regexp, replacement_string):
    return regexp.sub(replacement_string, string)


def main():
    parser = get_parser()
    args = parser.parse_args()
    contents = []
    if args.files:
        if args.files[0] == "-":
            contents.append(sys.stdin.read())
        else:
            for filename in args.files:
                with open(filename, "r") as f:
                    contents.append(f.read())

    for c in contents:
        s = build_stanza(
            c, regexps=args.regexps, comments=args.comments, sort=args.sort
        )

        s = stringify_stanza(
            s,
            normal=args.normal,
            linenum=args.linenum,
            seqnum=args.seqnum,
            delimiter=args.delimiter,
        )

        if args.replace:
            for regexp, replacement_string in args.replace:
                s = replace_pattern(s, regexp, replacement_string)

        if args.hash:
            h = getattr(hashlib, args.hash_algo)
            print(h(s.encode("utf-8")).hexdigest())
        else:
            print(s)


if __name__ == "__main__":
    main()
