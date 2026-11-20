import queue


def check_ordering(ord, adj):

    # check for cycles/non-connected graph
    if len(ord) != len(adj):
        return False

    # check if adjacent nodes connected
    for x in range(1, len(ord)):
        if ord[x] not in adj[ord[x-1]]:
            return False
    return True


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

# build adj list
adj = []
for _ in range(n):
    adj.append([])
for _ in range(m):
    x, y = list(map(int, input().split()))
    adj[x - 1].append(y - 1)  # convert from 1-indexed vertices to 0-indexed

ord = topsort_bfs(adj)

# check the normal case where there is a valid Hamiltonian path already
if check_ordering(ord, adj):
    for node in ord:
        print(node+1, end=' ')  # convert from 0-index to 1-index
    exit(0)

# add every single possible edge and check that this results in a DAG with Hamiltonian (way too slow, in the order of
# O((V+E)(V^2))
for x in range(n):
    for y in range(n):
        if x==y:
            continue

        # check that the edge doesn't already exist
        if y not in adj[x]:
            adj[x].append(y)
            ord = topsort_bfs(adj)
            if check_ordering(ord, adj):
                print("POSSIBLE")
                print(x+1, y+1)  # convert from 0-index to 1-index
                exit(0)
            adj[x].pop()

print("IMPOSSIBLE")