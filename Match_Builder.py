detail_to_node={}
matchlist=[]
newmatchlist=[]
nodes = []
# class Node:
#    def __init__(self, round, val, detail):
#       self.p1 = None
#       self.p2 = None
#       self.par = None
#       self.round = round
#       self.val = val
#       self.detail= detail
def comp(data):
    return data['seed']
def treefunc(root,data,cround):
    if nodes[root]["round"] > 2:
        #nn1= Node(root.round-1,root.val,None)
        nn1 = len(nodes)
        nodes.append({"p1": None, "p2": None, "par": None, "detail": None, "round": nodes[root]["rount"] - 1, "val": nodes[root]["val"]})
        #nn2 = Node(root.round-1,pow(2,cround)+1-root.val,None)
        nn2 = len(nodes)
        nodes.append({"p1": None, "p2": None, "par": None, "detail": None, "round": nodes[root]["round"] - 1, "val": pow(2, cround) + 1 - nodes[root]["val"]})
        #root.p1=nn1
        nodes[root]["p1"] = nn1
        #root.p2=nn2
        nodes[root]["p2"] = nn2
        #nn1.par=root
        nodes[nn1]["par"] = root
        #nn2.par=root
        nodes[nn2]["par"] = root
        treefunc(nn1,data,cround+1)
        treefunc(nn2,data,cround+1)
    elif nodes[root]["round"] == 2:
        if pow(2,cround)+1-nodes[root]["val"] <= len(data):
            num=pow(2,cround)+1-nodes[root]["val"]
            #nn1= Node(root.round-1,root.val,data[root.val-1])
            nn1 = len(nodes)
            nodes.append({"p1": None, "p2": None, "par": None, "detail": data[nodes[root]["val"] - 1], "round": nodes[root]["round"] - 1, "val": nodes[root]["val"]})
            #nn2= Node(root.round-1,num,data[num-1])
            nn2 = len(nodes)
            nodes.append({"p1": None, "p2": None, "par": None, "detail": data[num - 1], "round": nodes[root]["round"] - 1, "val": num})
            detail_to_node[(nodes[nn1]["detail"]['id'],nodes[nn1]["detail"]['seed'])]=nn1
            detail_to_node[(nodes[nn2]["detail"]['id'],nodes[nn2]["detail"]['seed'])]=nn2
            matchlist.append((nodes[nn1]["detail"],nodes[nn2]["detail"]))
            #root.p1=nn1
            nodes[root]["p1"] = nn1
            #root.p2=nn2
            nodes[root]["p2"] = nn2
            #nn1.par=root
            nodes[nn1]["par"] = root
            #nn2.par=root
            nodes[nn2]["par"] = root
            #print(nn1.detail['id'],nn1.detail['seed'])
            #print(nn2.detail['id'],nn2.detail['seed'])
        else:
            #root.detail=data[root.val-1]
            nodes[root]["detail"] = data[nodes[root]["val"] - 1]
            #detail_to_node[(root.detail['id'],root.detail['seed'])]=root
            detail_to_node[(nodes[root]["detail"]['id'], nodes[root]["detail"]["seed"])] = root
            #print(root.detail['id'],root.detail['seed'])
def func(data):
    data.sort(key=comp)
    for x in range(len(data)):
        data[x]['seed']=x+1
    num=1
    rounds=1
    while num<len(data):
        num=num*2
        rounds=rounds+1
    #root=Node(rounds,1,None)
    root = 1
    global nodes
    nodes = [{}, {"p1": None, "p2": None, "par": None, "detail": None, "round": rounds, "val": 1}]
    head=root
    treefunc(root,data,1)
def modify_winner(p1,p2,winner):
    temp1=detail_to_node[(p1['id'],p1['seed'])]
    temp2=detail_to_node[(p2['id'],p2['seed'])]
    #temp= temp1.par
    temp = nodes[temp1]["par"]
    #temp.detail= winner
    nodes[temp]["detail"] = winner
    detail_to_node[(p1['id'],p1['seed'])]=None
    detail_to_node[(p2['id'],p2['seed'])]=None
    detail_to_node[(winner['id'],winner['seed'])]=temp
    #temp_par=temp.par
    temp_par = nodes[temp]["par"]
    #temp_par_child1=temp_par.p1
    if (temp_par != None):
        temp_par_child1 = nodes[temp_par]["p1"]
        #temp_par_child2=temp_par.p2
        temp_par_child2 = nodes[temp_par]["p2"]
        if ((temp_par_child1 != None) and (temp_par_child2 != None)):
            newmatchlist.append((nodes[temp_par_child1]["detail"],temp_par_child2.detail))
    #temp.p1=None
    nodes[temp]["p1"] = None
    #temp.p2=None
    nodes[temp]["p2"] = None
def change_round():
    matchlist= newmatchlist
    newmatchlist.clear()
