import re

from cfgformalizer.cisco.statement import Statement
from cfgformalizer.stanza import Stanza


def depth(str):
    return len(str) - len(str.lstrip(" "))


class Cisco:
    @classmethod
    def parse(self, string):
        stanza = []
        prev_line = ""
        prev_line_depth = 0
        context = []
        current_context_depth = 0
        banner_delimiter = None
        linenum = 1
        seqnum = 0
        stanza = Stanza()

        banner_regexp = re.compile(r"(?:(?:banner(?:\smotd)?|fail-message)\s(\S))")

        for line in string.splitlines():
            line_depth = depth(line)
            line = line.rstrip().lstrip()

            # skip empty lines
            if line in ["\n", "\r\n"]:
                next

            # detect banner delimiter character
            if re.match(banner_regexp, line):
                m = re.match(banner_regexp, line)
                banner_delimiter = m.group(1)
                statement = Statement(linenum, 0, [], 0, line)
                stanza.append(statement)
                del context[:]
                context.append(line.split(banner_delimiter)[0] + banner_delimiter)
                prev_line = ""
                continue

            # append banner context to end of banner
            if banner_delimiter is not None and line.startswith(banner_delimiter):
                banner_delimiter = None
                seqnum += 1
                statement = Statement(linenum, seqnum, context.copy(), 0, "")
                stanza.append(statement)
                del context[:]
                seqnum = 0
                continue

            # end-policy, end-set, end-group
            if re.match(r"^end\-", line):
                statement = Statement(linenum, seqnum, context.copy(), line_depth, line)
                stanza.append(statement)
                del context[:]
                seqnum = 0
                continue

            # if RPL we dont stack up the previous line
            if len(context) >= 1:
                if re.match(r"^route-policy", context[0]):
                    seqnum += 1

            # normal case : push and pop context on the fly
            if line_depth == 0 and banner_delimiter is None:
                del context[:]
                seqnum = 0
                current_context_depth = 0

            elif line_depth >= prev_line_depth + 1:
                context.append(prev_line)
                current_context_depth = prev_line_depth
                seqnum += 1

            elif line_depth <= prev_line_depth - 1:
                # we pop n elements depending on the diff in line level
                if current_context_depth > line_depth:
                    del context[-1:]
                    current_context_depth = line_depth
                    seqnum += 1
                # we pop only once normally
                elif line_depth == current_context_depth:
                    context.pop()
                    seqnum += 1
                # sometimes we don't pop
                else:
                    seqnum += 1
            else:
                seqnum += 1

            statement = Statement(linenum, seqnum, context.copy(), line_depth, line)

            stanza.append(statement)
            prev_line_depth = line_depth
            prev_line = line.rstrip().lstrip()
            linenum += 1

        return stanza
