import hashlib
import re

from cfgformalizer.decorators import clone


class Stanza:
    def __init__(self, l=None):
        self.statements = l or []

    def __str__(self):
        s = [str(statement) for statement in self.statements]
        return "\n".join(s)

    def __eq__(self, other):
        return self.hash() == other.hash()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, statement):
        return statement in self.statements

    def __iter__(self):
        return iter(self.statements)

    def __len__(self):
        return len(self.statements)

    def __getitem__(self, index):
        return self.statements[index]

    def append(self, statement):
        self.statements.append(statement)

    def contexts(self):
        return [statement.context for statement in self.statements]

    @clone
    def like(self, regexp):
        self.statements = [
            statement
            for statement in self.statements
            if regexp.search(statement.formal())
        ]

    @clone
    def unlike(self, regexp):
        self.statements = [
            statement
            for statement in self.statements
            if not regexp.search(statement.formal())
        ]

    @clone
    def sort(self):
        self.statements = sorted(self.statements)

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

    def hash(self, algorithm=None):
        a = algorithm or "sha256"
        if a not in list(hashlib.algorithms_available):
            raise Exception("algorithm {} is not supported".format(a))
        h = getattr(hashlib, a)
        return h(self.formal().encode("utf-8")).hexdigest()
