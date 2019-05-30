import hashlib
import re

from cfgformalizer.decorators import clone


class Stanza:
    def __init__(self, l=None):
        self.statements = l or []

    def __str__(self):
        s = [str(statement) for statement in self.statements]
        return "\n".join(s)

    def append(self, statement):
        self.statements.append(statement)

    @clone
    def like(self, regexp):
        self.statements = [
            statement
            for statement in self.statements
            if re.search(regexp, statement.formal())
        ]

    @clone
    def unlike(self, regexp):
        self.statements = [
            statement
            for statement in self.statements
            if not re.search(regexp, statement.formal())
        ]

    @clone
    def without_comments(self):
        self.statements = [
            statement for statement in self.statements if not statement.is_comment()
        ]

    def normal(self, linenum=False, seqnum=False, delimiter=" "):
        s = [
            statement.normal(linenum, seqnum, delimiter)
            for statement in self.statements
        ]
        return "\n".join(s)

    def formal(self, linenum=False, seqnum=False, delimiter=" "):
        s = [
            statement.formal(linenum, seqnum, delimiter)
            for statement in self.statements
        ]
        return "\n".join(s)
