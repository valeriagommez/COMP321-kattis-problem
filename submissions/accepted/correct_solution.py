import queue
import sys


def find_sink(a, b, adj, ind, n):
    """
    Given 2 nodes a and b, decide if connecting the "sink" of node a to node b results in a correct solution. The sink
    is the last node to be processed in the topological sort excluding node b. Returns [-1] if it is not possible and
    the edge if it is.
    """

    # continue the topological sort, excluding node b
    q = queue.Queue()
    q.put(a)

    # x is a's "sink"
    x = -1
    while not q.empty():
        x = q.get()
        n-=1
        for node in adj[x]:
            ind[node] -= 1

            # put node in queue if it is a source
            if ind[node] == 0:
                q.put(node)

        # if no items in q, we have reached the "sink" of node a
        if q.qsize() == 0:
            break

        # if we encounter 2 sources, we cannot cover all the nodes in one path (we are forced to choose one or the
        # other), since we are already using our one edge to cover a and b in one pass, this makes it impossible
        elif q.qsize() > 1:
            return [-1]

    # continue topological sort with b as the source, this simulates going from a's "sink" x to b, which is the edge
    # we are trying to add
    q.put(b)
    while not q.empty():
        top = q.get()
        n-=1
        for node in adj[top]:
            ind[node] -= 1

            # put node in queue if it is a source
            if ind[node] == 0:
                q.put(node)

        # we have reached the end if the queue is empty
        if q.qsize() == 0:
            break

        # again, if we encounter more than 2 source nodes a hamiltonian path is impossible
        elif q.qsize() > 1:
            return [-1]

    # the parameter n checks that all the nodes are used up, this also checks that there are no cycles
    if n==0:
        return [x, b]

    # if not all the nodes covered, this fails
    else:
        return [-1]


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
        size = q.qsize()

        # if there are 2 sources, we cannot cover all the nodes in a single path since at some point we must choose
        # one of these sources and cannot return to the other one, so in that case we try to add the edge from the
        # "sink" of a to b (or vice versa) in order to cover a and all nodes after it, then b and all nodes after it
        if size == 2:
            a = q.get()
            b = q.get()

            # try to add the edge from a's sink to b, if this fails try to add the edge from b's sink to a
            e = find_sink(a, b, list(adj), list(ind), len(adj)-len(ord))
            if e != [-1]:
                return [-1, e[0], e[1]]
            else:
                e = find_sink(b, a, list(adj), list(ind), len(adj)-len(ord))
                if e == [-1]:
                    return [-1]
                return [-1, e[0], e[1]]

        # if there are more than 2 nodes, adding 1 edge is not enough to cover the entire graph in one path
        elif size > 2:
            print("IMPOSSIBLE")
            exit(0)
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
    adj[x-1].append(y-1)  # convert from 1-indexed vertices to 0-indexed

# get order using topological sort, if the graph has cycles, len(ord) != len(adj)
ord = topsort_bfs(adj)

# this is the special case where we need to add an edge which we indicate by returning [-1, u, v] where the edge to
# be added is (u, v)
if len(ord)>1 and ord[0] == -1:
    print("POSSIBLE")
    print(ord[1]+1, ord[2]+1)  # convert from 0-index to 1-index

# check for no cycles
elif len(ord) != len(adj):
    print("IMPOSSIBLE")
else:
    # if all the adjacent nodes in the topological sort are connected, then there exists a Hamiltonian path
    for x in range(1, len(ord)):

        # ord[x] not in ord[x-1]'s adjacency list, so they are not connected
        if ord[x] not in adj[ord[x - 1]]:
            print("IMPOSSIBLE")
            exit(0)
    for node in ord:
        print(node + 1, end=' ')  # convert from 0-index to 1-index
