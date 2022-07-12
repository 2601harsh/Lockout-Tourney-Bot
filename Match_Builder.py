detail_to_node={}
matchlist=[]
newmatchlist=[]
nodes = []
def comp(data):
    return data['seed']
def treefunc(root,data,cround):
    if nodes[root]["round"] > 2:
        nn1 = len(nodes)
        nodes.append({"p1": None, "p2": None, "par": None, "detail": None, "round": nodes[root]["round"] - 1, "val": nodes[root]["val"]})
        nn2 = len(nodes)
        nodes.append({"p1": None, "p2": None, "par": None, "detail": None, "round": nodes[root]["round"] - 1, "val": pow(2, cround) + 1 - nodes[root]["val"]})
        nodes[root]["p1"] = nn1
        nodes[root]["p2"] = nn2
        nodes[nn1]["par"] = root
        nodes[nn2]["par"] = root
        treefunc(nn1,data,cround+1)
        treefunc(nn2,data,cround+1)
    elif nodes[root]["round"] == 2:
        if pow(2,cround)+1-nodes[root]["val"] <= len(data):
            num=pow(2,cround)+1-nodes[root]["val"]
            nn1 = len(nodes)
            nodes.append({"p1": None, "p2": None, "par": None, "detail": data[nodes[root]["val"] - 1], "round": nodes[root]["round"] - 1, "val": nodes[root]["val"]})
            nn2 = len(nodes)
            nodes.append({"p1": None, "p2": None, "par": None, "detail": data[num - 1], "round": nodes[root]["round"] - 1, "val": num})
            detail_to_node[(nodes[nn1]["detail"]['id'],nodes[nn1]["detail"]['seed'])]=nn1
            detail_to_node[(nodes[nn2]["detail"]['id'],nodes[nn2]["detail"]['seed'])]=nn2
            matchlist.append((nodes[nn1]["detail"],nodes[nn2]["detail"]))
            nodes[root]["p1"] = nn1
            nodes[root]["p2"] = nn2
            nodes[nn1]["par"] = root
            nodes[nn2]["par"] = root
        else:
            nodes[root]["detail"] = data[nodes[root]["val"] - 1]
            detail_to_node[(nodes[root]["detail"]['id'], nodes[root]["detail"]["seed"])] = root
def func(data):
    data.sort(key=comp)
    for x in range(len(data)):
        data[x]['seed']=x+1
    num=1
    rounds=1
    while num<len(data):
        num=num*2
        rounds=rounds+1
    root = 1
    global nodes
    nodes = [{}, {"p1": None, "p2": None, "par": None, "detail": None, "round": rounds, "val": 1}]
    head=root
    treefunc(root,data,1)
def modify_winner(p1,p2,winner):
    temp1=detail_to_node[(p1['id'],p1['seed'])]
    temp2=detail_to_node[(p2['id'],p2['seed'])]
    temp = nodes[temp1]["par"]
    nodes[temp]["detail"] = winner
    detail_to_node[(p1['id'],p1['seed'])]=None
    detail_to_node[(p2['id'],p2['seed'])]=None
    detail_to_node[(winner['id'],winner['seed'])]=temp
    temp_par = nodes[temp]["par"]
    if (temp_par != None):
        temp_par_child1 = nodes[temp_par]["p1"]
        temp_par_child2 = nodes[temp_par]["p2"]
        if ((temp_par_child1 != None) and (temp_par_child2 != None)):
            newmatchlist.append((nodes[temp_par_child1]["detail"],nodes[temp_par_child2]["detail"]))
    nodes[temp]["p1"] = None
    nodes[temp]["p2"] = None
def change_round():
    global matchlist
    matchlist= newmatchlist
    newmatchlist.clear()
