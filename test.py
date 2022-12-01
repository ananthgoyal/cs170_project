import pty
from starter import *
from networkx.algorithms import tree
import copy
import metis
import itertools
import warnings
from signal import signal, SIGSEGV

warnings.filterwarnings("ignore")
def handler(sigNum, frame):
    print("handle signal", sigNum)


def part2(G:nx.Graph, cuts = 2):
    G_prime = copy.deepcopy(G)  
    num_nodes = G_prime.number_of_nodes()
    for i in range(num_nodes):
        for j in range(i, num_nodes):
            if not G_prime.has_edge(i, j):
                #pass
                G_prime.add_edge(i, j, weight = 1001)
            else:
                G_prime.add_edge(i, j, weight = 1001 - G_prime[i][j]['weight'])
    
    scoreSet = []
    partSet = []
    parts = []
    

    
def greedy(G:nx.Graph, cuts = 10):
    sol = [[] for i in range(cuts)]
    G_prime = copy.deepcopy(G)
    num_nodes = G.number_of_nodes()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if not G_prime.has_edge(i, j):
                G_prime.add_edge(i, j, weight = 1)
            else:
                #G_prime.remove_edge(i, j)
                pass
    

    '''print(list(tree))
    lst = list(sum(tree, ()))
    mx = max(set(lst), key=lst.count)
    print(mx)
    print(G.degree(mx))

    for edge in G_prime.edges(8):
        print(edge)

    print(min(G_prime.nodes(), key=lambda x: G_prime.degree(x)))'''


    
    
    i = 0
    st = []
    while True:
    #for x in range(200):
        tree = nx.minimum_spanning_edges(G_prime, weight='weight', data=False)
        #print(list(tree))
        lst = list(sum(tree, ()))
        #print(lst)
        if (len(lst) == 2):
            G.nodes[lst[0]]['team'] = i % cuts + 1
            G.nodes[lst[1]]['team'] = (i + 1) % cuts + 1
        if not lst:
            break
        mx = max(set(lst), key=lst.count)
        #print(lst)
        #print(mx)
        G_prime.remove_node(mx)
        G.nodes[mx]['team'] = i % cuts + 1
        st.append(mx)
        #print(G.nodes[mx]['team'])
        i += 1
    print(score(G))
    return G

    


def part(G:nx.Graph, cuts = 2):
    G_prime = copy.deepcopy(G)
    G_prime.graph['edge_weight_attr'] = 'weight'
    num_nodes = G_prime.number_of_nodes()

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if not G_prime.has_edge(i, j):
                #pass
                G_prime.add_edge(i, j, weight = 1001)
            else:
                #G_prime.add_edge(i, j, weight = 1001 - G_prime[i][j]['weight'])
                G_prime.remove_edge(i, j)# , weight = 1001 - G_prime[i][j]['weight'])

    scoreSet = []
    partSet = []

    
    for sd in range(1, 3):
        val, parts = metis.part_graph(
            G_prime, cuts, recursive=True,ncuts = 100, tpwgts=[(1/cuts) for _ in range(cuts)], niter = 100, iptype='random', seed=sd, contig=True)
        for i in range(len(parts)):
            G.nodes[i]['team'] = parts[i] + 1
        scr = score(G)
        #visualize(G_prime)
        scoreSet.append(scr)
        partSet.append(parts)
        print(scr)
        if scr < 1000:
            break
        #return G
    
    minIND = scoreSet.index(min(scoreSet))
    for i in range(len(partSet[minIND])):
        G.nodes[i]['team'] = partSet[minIND][i] + 1
    return partSet[minIND], min(scoreSet)

def solve2(G: nx.Graph, targ=2):
    partSet = []
    scoreSet = []
    i = 0
    numNodes = G.number_of_nodes()
    '''if targ:
        part(G, cuts=targ)
        return G'''
    for i in range(2, 20):
        pS, sS = part(G, cuts=i)
        #part2(G, cuts=i)
        '''if (i > 2 and sS > min(scoreSet)):
            #ind = i - 3
            #print(ind)
            for j in range(len(partSet[-1])):
                G.nodes[j]['team'] = partSet[-1][j] + 1
            return G'''
        partSet.append(pS)
        scoreSet.append(sS) 
        if sS < 1000:
            break     
    minIND =  scoreSet.index(min(scoreSet))
    for i in range(len(partSet[minIND])):
        G.nodes[i]['team'] = partSet[minIND][i] + 1
    return G


#G = read_input('inputs_170/medium249.in')
#visualize(G)
#run(solve2, 'inputs_170/medium249.in', 'outputs_170/medium249.out', overwrite=True)
#run(solve2, 'inputs_170/large225.in', 'outputs_170/large225.out', overwrite=True)
#greedy(G)
run(solve2, 'inputs_170/medium17.in', 'outputs_170/medium.out', overwrite=True)

#run_vis(solve2, 'inputs_170/medium17.in', 'large.out', overwrite=True)

#run_all(solve2, 'inputs_170', 'complete', overwrite=True)
#tar('complete', overwrite=True)
