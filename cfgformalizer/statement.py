class Statement:
    def __init__(self, lineno, seqnum, context, depth, string):
        self.lineno = lineno
        self.seqnum = seqnum
        self.context = context
        self.depth = depth
        self.string = string
