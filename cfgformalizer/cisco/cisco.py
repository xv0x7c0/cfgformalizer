from cfgformalizer.cisco.statement import Statement
from cfgformalizer.stanza import Stanza
import re


def depth(str):
    return len(str) - len(str.lstrip(" "))


class Cisco:
    @classmethod
    def parse(self, io):
        stanza = []
        prev_line = ""
        prev_line_depth = 0
        statement_context = []
        current_context_depth = 0
        statement_seqnum = 0
        banner_delimiter = None
        lineno = 1
        stanza = Stanza()

        banner_regexp = re.compile(r"(?:(?:banner(?:\smotd)?|fail-message)\s(\S))")

        for line in io.readlines():
            line_depth = depth(line)
            line = line.rstrip().lstrip()

            # skip empty lines
            if line in ["\n", "\r\n"]:
                next

            # detect banner delimiter character
            if re.match(banner_regexp, line):
                m = re.match(banner_regexp, line)
                banner_delimiter = m.group(1)
                statement = Statement(lineno, 0, [], 0, line)
                stanza.append(statement)
                del statement_context[:]
                statement_context.append(
                    line.split(banner_delimiter)[0] + banner_delimiter
                )
                prev_line = ""
                continue

            # append banner context to end of banner
            if banner_delimiter is not None and line.startswith(banner_delimiter):
                banner_delimiter = None
                statement_seqnum += 1
                statement = Statement(
                    lineno, statement_seqnum, statement_context.copy(), 0, ""
                )
                stanza.append(statement)
                del statement_context[:]
                statement_sequence = 0
                continue

            # end-policy, end-set, end-group
            if re.match(r"^end\-", line):
                statement = Statement(
                    lineno, statement_seqnum, statement_context.copy(), line_level, line
                )
                stanza.append(statement)
                del statement_context[:]
                statement_sequence = 0
                continue

            # if RPL we dont stack up the previous line
            if len(statement_context) >= 1:
                if re.match(r"^route-policy", statement_context[0]):
                    statement_sequence += 1

            # normal case : push and pop context on the fly
            if (line_depth == 0 or line.startswith("!")) and banner_delimiter is None:
                del statement_context[:]
                statement_seqnum = 0
                current_context_depth = 0

            elif line_depth >= prev_line_depth + 1:
                statement_context.append(prev_line)
                current_context_depth = prev_line_depth
                statement_seqnum += 1

            elif line_depth <= prev_line_depth - 1:
                # we pop n elements depending on the diff in line level
                if current_context_depth > line_depth:
                    del statement_context[-1:]
                    current_context_depth = line_depth
                    statement_seqnum += 1
                # we pop only once normally
                elif line_depth == current_context_depth:
                    statement_context.pop()
                    statement_seqnum += 1
                # sometimes we don't pop
                else:
                    statement_seqnum += 1

            statement = Statement(
                lineno, statement_seqnum, statement_context.copy(), line_depth, line
            )

            stanza.append(statement)
            prev_line_depth = line_depth
            prev_line = line.rstrip().lstrip()
            lineno += 1

        return stanza
