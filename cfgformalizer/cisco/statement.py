from cfgformalizer.statement import Statement


class Statement(Statement):
    def formal(self, lineno=False, sequence=False, delimiter=" "):
        s = []
        if lineno:
            s.append("%6s" % self.lineno)
        if sequence:
            s.append("%6s" % self.sequence)
        if len(self.context) == 0:
            s.append(self.string)
        else:
            s.append(delimiter.join(self.context))
            s.append(delimiter)
            s.append(self.string)
        return "".join(s)
