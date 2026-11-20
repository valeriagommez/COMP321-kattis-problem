#include <vector>
#include <iostream>
#include <queue>
#include <algorithm>
#include <fstream>

using namespace std;


/*
Given 2 nodes a and b, decide if connecting the "sink" of node a to node b results in a correct solution. The sink
    is the last node to be processed in the topological sort excluding node b. Returns [-1] if it is not possible and
    the edge if it is.
*/
vector<int> find_sink(int a, int b, vector<vector<int>> adj, vector<int> ind, int n){

    // continue the topological sort, excluding node b
    queue<int> q;
    q.push(a);

    // x is a's "sink"
    int x = -1;
    while (!q.empty()){
        x = q.front();
        q.pop();
        n--;
        for (int node : adj[x]){
            ind[node]--;

            // put node in queue if it is a source
            if (ind[node]==0) q.push(node);
        }

        // if no items in q, we have reached the "sink" of node a
        if (q.empty()) break;

        // if we encounter 2 sources, we cannot cover all the nodes in one path (we are forced to choose one or the other), 
        // since we are already using our one edge to cover a and b in one pass, this makes it impossible
        else if (q.size()>1) return {-1};
    }

    // continue topological sort with b as the source, this simulates going from a's "sink" x to b, which is the edge we are trying to add
    q.push(b);
    int top;
    while (!q.empty()){
        top = q.front();
        q.pop();
        n--;
        for (int node : adj[top]){
            ind[node]--;

            // put node in queue if it is a source
            if (ind[node]==0) q.push(node);
        }

        // we have reached the end if the queue is empty
        if (q.empty()) break;

        // again, if we encounter more than 1 source node a hamiltonian path is impossible
        else if (q.size()>1) return {-1};
    }

    // the parameter n checks that all the nodes are used up, this also checks that there are no cycles
    if (n==0) return {x, b};

    // if not all the nodes covered, this fails
    else return {-1};
}

// Kahn's algorithm
vector<int> topsort_bfs(vector<vector<int>> adj){
    int n = adj.size();
    vector<int> ind(n);
    vector<int> ord;
    queue<int> q;

    // count indegrees of each node
    for (vector<int> a : adj){
        for (int node : a) ind[node]++;
    }

    // put 0-indegree nodes into the queue
    for (int x=0; x<n; x++){
        if (ind[x] == 0) q.push(x);
    }
    int top;

    // perform bfs
    int s;
    while (!q.empty()){
        s = q.size();

        /*
        if there are 2 sources, we cannot cover all the nodes in a single path since at some point we must choose
        one of these sources and cannot return to the other one, so in that case we try to add the edge from the
        "sink" of a to b (or vice versa) in order to cover a and all nodes after it, then b and all nodes after it
        */
        if (s==2){
            int a = q.front();
            q.pop();
            int b = q.front();
            q.pop();

            // try to add the edge from a's sink to b, if this fails try to add the edge from b's sink to a
            vector<int> e = find_sink(a, b, adj, ind, adj.size()-ord.size());
            if (e.size()>1) return {-1, e[0], e[1]};
            else{
                e = find_sink(b, a, adj, ind, adj.size()-ord.size());
                if (e.size()>1) return {-1, e[0], e[1]};
                return {-1};
            }
        }

        // if there are more than 2 source nodes, adding 1 edge is not enough to cover the entire graph in one path
        else if (s>2) return {-1};

        // add sources to q
        top = q.front();
        q.pop();
        ord.push_back(top);
        for (int node : adj[top]){
            ind[node]--;  // update indegree
            if (ind[node] == 0) q.push(node);
        }
    }
    return ord;
}


int main(){
    int n;
    int m;
    cin >> n >> m;

    // edge case: only 1 node, so only 1 path just containing that node
    if (n==1){
        cout << 1;
        return 0;
    }

    // build adj list
    vector<vector<int>> adj;
    for (int x=0; x<n; x++){
        adj.push_back({});
    }
    int x;
    int y;
    for (int i=0; i<m; i++){
        cin >> x >> y;
        adj[x-1].push_back(y-1);  // convert from 1-indexed vertices to 0-indexed
    }

    // get order using topological sort, if the graph has cycles, len(ord) != len(adj)
    vector<int> ord = topsort_bfs(adj);

    // this is the special case where we need to add an edge which we indicate by returning [-1, u, v] where the edge to be added is (u, v)
    if (ord.size()>1 && ord[0] == -1){
        cout << "POSSIBLE\n" << ord[1]+1 << ' ' << ord[2]+1;
    }

    // check for no cycles
    else if (ord.size() != n){
        cout << "IMPOSSIBLE";
        return 0;
    }

    else{

        // if all the adjacent nodes in the topological sort are connected, then there exists a Hamiltonian path
        vector<int> v;
        for (int x=1; x<n; x++){

            // ord[x] not in ord[x-1]'s adjacency list, so they are not connected
            v = adj[ord[x-1]];
            if (find(v.begin(), v.end(), ord[x]) == v.end()){
                cout << "IMPOSSIBLE";
                return(0);
            }
        }
        for (int node : ord){
            cout << node+1 << ' '; // convert from 0-indexed vertices to 1-indexed
        }
    }
}
