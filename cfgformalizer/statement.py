class Statement:
    def __init__(self, linenum, seqnum, context, depth, string):
        self.linenum = linenum
        self.seqnum = seqnum
        self.context = context
        self.depth = depth
        self.string = string
