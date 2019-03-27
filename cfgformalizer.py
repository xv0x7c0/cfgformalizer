#!/usr/bin/env python
from cfgformalizer.statement import Statement
from cfgformalizer.stanza import Stanza
import re

def depth(str):
  return len(str) - len(str.lstrip(' '))

f = open('examples/config.txt', 'r')
lines = f.readlines()

stanza = []
prev_line = ''
prev_line_depth = 0
statement_context = []
current_context_depth = 0
statement_seqnum = 0
banner_delimiter = None
lineno = 1
stanza = Stanza()

for line in lines:
  line_depth = depth(line)
  line = line.rstrip()

  if line_depth == 0 or line.startswith('!'):
    del statement_context[:]
    statement_seqnum = 0
    current_context_depth = 0

  elif line_depth >= prev_line_depth + 1:
    statement_context.append(prev_line)
    current_context_depth = prev_line_depth
    statement_seqnum += 1

  elif line_depth <= prev_line_depth - 1:
    if current_context_depth > line_depth:
      del(statement_context[-1:])
      current_context_depth = line_depth
      statement_seqnum += 1

    elif line_depth == current_context_depth:
      statement_context.pop()
      statement_seqnum += 1
    else:
      statement_seqnum += 1
  
  statement = Statement(lineno, statement_seqnum, statement_context.copy(), depth, line)

  stanza.append(statement)
  prev_line_depth = line_depth
  prev_line = line.rstrip().lstrip()
  lineno += 1


for s in stanza.statements:
  print(' '.join(s.context) + s.string)
