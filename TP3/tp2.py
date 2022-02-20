def label(G,k):
    return(G.nodes[k]['label'][0])


def cost_node(G1,G2):
    nb_node1=G1.number_of_nodes()
    nb_node2=G2.number_of_nodes()
    C=np.full((nb_node1+1,nb_node2+1),0)
    for k in range (0,nb_node1-1):
        for i in range (0,nb_node2-1):
            C[k][i]=node_cost[dict[label(G1,k)]][dict[label(G2,i)]]
    for k in range (nb_node1):
        C[k][nb_node2]=node_del
    for i in range (nb_node2):
        C[nb_node1][i]=node_ins
    C[nb_node1][nb_node2]=0
       
    return C

def type(G,e):
    return(int(G.edges[e]['bond_type']))


def cost_map_edge(G1,G2,i,j,edge_cost,edge_del,edge_ins):
    edge_i=[]
    edge_j=[]
    
    edge_i=G1.edges(i)   
    edge_j=G2.edges(j)
    # initialisation of both lists edge_i and edge_j
    

    
    ni=len(edge_i)
    nj=len(edge_j)
    
    
    C=np.full((ni+1,nj+1),0.0)
    #initialization of C. To be completed.

    
    #for e in edge_i:
     #   print(G1.edges[e]['bond_type']) 
    i,j=0,0
    for ei in edge_i:
        j=0
        C[i][nj]=edge_del
        for ej in edge_j:
            C[i][j]=edge_cost[type(G1,ei)][type(G2,ej)]
            j+=1
        i+=1
        
    for j in range(nj):
        C[i][nj]=edge_ins
    
    #application of the Hungarian algortithm on C.
    result=gedlibpy.hungarian_LSAPE(C)
    
    cost=np.array(result[2]).sum()+np.array(result[3]).sum()
    return cost

def cost_edge(G1,G2,edge_cost,edge_del,edge_ins):
    nb_node1=G1.number_of_nodes()
    nb_node2=G2.number_of_nodes()
    C=np.full((nb_node1+1,nb_node2+1),0.0)

                   
    #to be completed
    for n1 in nx.nodes(G1):
        for n2 in nx.nodes(G2):
            C[n1][n2]=cost_map_edge(G1,G2,n1,n2,edge_cost,edge_del,edge_ins)
                          
    
    for i in range(nb_node1):
        C[i][nb_node2] = len(G1.edges(i))*edge_del
    
    for j in range(nb_node2):
        C[nb_node1][j] = len(G2.edges(j))*edge_ins
    
    return C

def compute_graph_mapping(C):
    result=gedlibpy.hungarian_LSAPE(C)
    cost=np.array(result[2]).sum()+np.array(result[3]).sum()

    return result[0],result[1],cost

def from_mapping_function_to_matrix(rho,varrho):
    n=len(rho)
    m=len(varrho)
    X=np.zeros((n+1,m+1))
    for i in range(len(rho)):
        X[i,int(rho[i])] = 1
    for j in range(len(varrho)):
        X[int(var_rho[j]),j] = 1
    #to be completed
    return X

def ged_edge(G1,G2,rho,varrho,edge_cost,edge_del,edge_ins):
    edge_ged=0
    
    for e1 in nx.edges(G1):
        i,j=e1[0],e1[1]
        k,l=rho[i],rho[j]
        if k not in nx.nodes(G2) or l not in nx.nodes(G2):
            edge_ged+=edge_del
        elif (k,l) in nx.edges(G2):
            edge_ged+=edge_cost[type(G1,(i,j))][type(G2,(k,l))]
        elif(k,l) not in nx.edges(G2):
            edge_ged+=edge_ins
    
    for e2 in nx.edges(G2):
        i,j=varrho[e2[0]],varrho[e2[1]]
        if i not in nx.nodes(G1) or j not in nx.nodes(G1):
            edge_ged+=edge_ins
        elif(i,j) not in nx.edges(G1):
            edge_ged+=edge_ins
              
    return edge_ged