from cfgformalizer.statement import Statement


class Statement(Statement):
    def __str__(self):
        return self.normal()

    def is_comment(self):
        if len(self.string) > 0:
            return self.string[0] == "!"

    def normal(self, linenum=False, seqnum=False, delimiter=" "):
        s = []
        if linenum:
            s.append("%6s" % self.linenum)
            s.append(delimiter)
        if seqnum:
            s.append("%6s" % self.seqnum)
            s.append(delimiter)
        s.append(self.depth * delimiter + self.string)
        return "".join(s)

    def formal(self, linenum=False, seqnum=False, delimiter=" "):
        s = []
        if linenum:
            s.append("%6s" % self.linenum)
            s.append(delimiter)
        if seqnum:
            s.append("%6s" % self.seqnum)
            s.append(delimiter)
        if len(self.context) == 0:
            s.append(self.string)
            s.append(delimiter)
        else:
            s.append(delimiter.join(self.context))
            s.append(delimiter)
            s.append(self.string)
        return "".join(s)
