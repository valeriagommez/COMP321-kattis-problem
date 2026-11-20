import queue
import sys


# Khan's algorithm
def topsort_bfs(adj):
    n = len(adj)
    ind = [0] * n
    ord = []
    q = queue.Queue()

    # compute indegree of all nodes
    for a in adj:
        for node in a:
            ind[node] += 1

    # put 0-indegree nodes in the queue
    for x in range(n):
        if ind[x] == 0:
            q.put(x)

    # perform bfs
    while not q.empty():
        top = q.get()
        ord.append(top)
        for node in adj[top]:
            ind[node] -= 1

            # add sources to q
            if ind[node] == 0:
                q.put(node)
    return ord


n, m = list(map(int, input().split()))

# edge case: only 1 node, so only 1 path just containing that node
if n == 1:
    print(1)
    exit(0)

# build adj list
adj = []
for _ in range(n):
    adj.append([])
for _ in range(m):
    x, y = list(map(int, input().split()))
    adj[x - 1].append(y - 1)  # convert from 1-indexed vertices to 0-indexed

# get order using topological sort, if the graph has cycles, len(ord) != len(adj)
ord = topsort_bfs(adj)

# check for no cycles
if len(ord) != len(adj):
    print("IMPOSSIBLE")
else:
    # if all the adjacent nodes in the topological sort are connected, then there exists a Hamiltonian path
    # this algorithm naively assumes that the added edge corresponds to exactly 1 gap in connection between 2
    # adjacent nodes in the ordering, which is not true for every ordering and there is no guarantee that you will
    # get an ordering where this is the case
    e = []
    for x in range(1, len(ord)):
        if ord[x] not in adj[ord[x - 1]]:
            if len(e) > 0:
                print("IMPOSSIBLE")
                exit(0)
            e = [ord[x-1], ord[x]]  # track disconnected nodes
    if len(e) > 0:
        print("POSSIBLE")
        print(e[0] + 1, e[1] + 1)  # convert from 0-index to 1-index
    else:
        for node in ord:
            print(node + 1, end=' ')  # convert from 0-index to 1-index
