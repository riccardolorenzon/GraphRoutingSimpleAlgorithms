'''
Created on 15/mar/2014

@author: riccardo
'''

from priodict import priorityDictionary
from collections import deque

def Dijkstra(graph, start, end=None):
    final_distances = {}    # dictionary of final distances
    predecessors = {}   
    estimated_distances = priorityDictionary()   # heap binary tree initialization
    
    estimated_distances[start] = 0
   
    oneHop = False
    hops = 0
    
    for vertex in estimated_distances:
        final_distances[vertex] = estimated_distances[vertex]
        if (vertex == end and oneHop): 
            break
        oneHop = True
        hops  = hops+1
        
        for edge in graph[vertex]:
            path_distance = final_distances[vertex] + graph[vertex][edge]
            if edge in final_distances:
                if path_distance < final_distances[edge]:
                    raise ValueError, \
                        "Dijkstra: found better path to already-final vertex"
                else:
                    if (final_distances[edge] == 0): #scenario node - node
                        final_distances[edge] = path_distance
            if edge not in estimated_distances or path_distance < estimated_distances[edge]:
                estimated_distances[edge] = path_distance
                predecessors[edge] = vertex

    return (final_distances,predecessors)

def BFS(graph,start,end,q, min_hops, max_hops):
    temp_path = [start]
    final_queue = deque()
    q.append(temp_path)
    while len(q) != 0:
        tmp_path = q.pop()
        last_node = tmp_path[len(tmp_path)-1]
        if last_node == end:
            final_queue.append(tmp_path)
        for link_node in graph[last_node]:
            if ( (len(tmp_path)<= max_hops)):
                new_path = tmp_path + [link_node]
                q.append(new_path)
    return final_queue
    
def shortestPath(graph,start,end):
    """
    Find a single shortest path from the given start vertex
    to the given end vertex.
    The input has the same conventions as Dijkstra().
    The output is a list of the vertices in order along
    the shortest path.
    """
    final_distances,predecessors = Dijkstra(graph,start,end)
    path = []
    while 1:
        path.append(end)
        if end == start: break
        end = predecessors[end]
    path.reverse()
    return path

def shortestPathWeight(graph,start,end):
    final_distances,predecessors = Dijkstra(graph,start,end)
    return final_distances[end]
    
    
def route(graph, route):
    distance = 0
    predecessor = route[0]
    for vertex in route:
        weight= 0;
        if(predecessor != vertex):
            if (vertex not in graph[predecessor]):
                return -1
            weight = graph[predecessor][vertex]
            predecessor = vertex
        
        distance = weight + distance
    return distance

def findAllPaths(graph, minHopsNumber, maxHopsNumber, start, end):
    q = deque()
    final_queue = BFS(graph,start,end,q, minHopsNumber, maxHopsNumber)
    s = ''
    i = 0
    while (len(final_queue) != 0):
        item = final_queue.pop()
        if (len(item) >= minHopsNumber and len(item) <= maxHopsNumber ):
            s = s + 'valid path : ' + str(item) + ' '
            i = i + 1
    return (s, i)
def main():
    G = {'A':{'B':5, 'E':7, 'D':5}, 'B':{'C':4}, 'C':{'D':8, 'E':2}, 'D':{'C':8, 'E':6}, 
         'E':{'B':3}}
    
    #questions 1-5:  Root is always node A, the constraint of the given route force to not use Dijkstra as 
    # the algorithm is really useful for finding all possible routes between two nodes.     
    questions = {}
    questions[1] =['A' , 'B' ,'C']
    questions[2] = ['A', 'D']
    questions[3] = ['A', 'D', 'C']
    questions[4] = ['A', 'E', 'B', 'C', 'D']
    questions[5] = ['A', 'E', 'D']
    
    for key in questions:
        distance = route(G, questions[key])
        if (distance == -1):
            print 'question ' + str(key) + ' NO SUCH ROUTE'
        else:
            print 'question ' + str(key) + ' distance is ' + str(distance)
    
    #quesyions 6,7 
    (s, i) = findAllPaths(G, 2, 4, 'C', 'C')
    print 'question 6 : ' + str(i) + ' paths: ' + s 
    
    (s, i) = findAllPaths(G, 5, 5 , 'A', 'C')
    print 'question 7 : ' + str(i) + ' paths: ' + s 
    
    #questions 8,9, straight application of (revisited for the node-node scenario) Dijkstra algorithm
    print 'question 8 ' + str(shortestPathWeight(G, 'B', 'B'))
    print 'question 9 ' + str(shortestPathWeight(G, 'A', 'C'))
    
if __name__ == "__main__":
    main()