#!/usr/bin/env python3

# This is a sample input validator, written in Python 3.

# Please refer to the comments in README.md for a description of the syntax it
# is validating. Then, change it as you need.

import sys
import re

first_line = sys.stdin.readline()
assert re.fullmatch(r'[1-9][0-9]* (0|[1-9][0-9]*)\n?', first_line) # 2 space separated integers (number of nodes and number of edges)
n, m = first_line.split()

n = int(n)
m = int(m)
assert 1 <= (n + m) <= 10**4 # explicit constraint from the problem description

unique_edges = set()
n_nodes = set()
for _ in range(m):
    edge_input = sys.stdin.readline()
    assert re.fullmatch(r'[1-9][0-9]* ([1-9][0-9]*)\n?', edge_input) # edge represented as 2 space separated integers (nodes), must have m edges
    n1, n2 = edge_input.split()
    n1 = int(n1)
    n2 = int(n2)
    assert n1 != n2 # edges have different origin and destination

    # verify edge uniqueness
    assert (n1, n2) not in unique_edges
    unique_edges.add((n1, n2))

    # verify count of nodes (max n unique nodes)
    n_nodes.add(n1)
    n_nodes.add(n2)
    assert len(n_nodes) <= n

# ensure no extra input
assert sys.stdin.readline() == ''

# if we get here, all is well
sys.exit(42)