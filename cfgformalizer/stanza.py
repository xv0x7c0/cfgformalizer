import re


class Stanza:
    def __init__(self, l=[]):
        self.statements = l.copy()

    def __str__(self):
        s = [str(statement) for statement in self.statements]
        return "\n".join(s)

    def append(self, statement):
        self.statements.append(statement)

    def like(self, regexp):
        return Stanza(
            [
                statement
                for statement in self.statements
                if re.search(regexp, statement.formal())
            ]
        )

    def without_comments(self):
        return Stanza(
            [statement for statement in self.statements if not statement.is_comment()]
        )

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
