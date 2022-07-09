play={}
class Node:
   def __init__(self, round, val, detail):
      self.p1 = None
      self.p2 = None
      self.par = None
      self.round = round
      self.val = val
      self.detail= detail
def comp(data):
    return data['seed']
def treefunc(root,data,cround):
    if root.round > 2:
        nn1= Node(root.round-1,root.val,None)
        nn2= Node(root.round-1,pow(2,cround)+1-root.val,None)
        play[(nn1,nn2)]=root
        root.p1=nn1
        root.p2=nn2
        nn1.par=root
        nn2.par=root
        treefunc(nn1,data,cround+1)
        treefunc(nn2,data,cround+1)
    elif root.round == 2:
        if pow(2,cround)+1-root.val <= len(data):
            num=pow(2,cround)+1-root.val
            nn1= Node(root.round-1,root.val,data[root.val-1])
            nn2= Node(root.round-1,num,data[num-1])
            root.p1=nn1
            root.p2=nn2
            nn1.par=root
            nn2.par=root
            #print(nn1.detail['id'],nn1.detail['seed'])
            #print(nn2.detail['id'],nn2.detail['seed'])
        else:
            root.detail=data[root.val-1]
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
    root=Node(rounds,1,None)
    head=root
    treefunc(root,data,1)
def modify_winner(p1,p2,winner):
    temp= play.get((p1,p2))
    if temp == None:
        return temp
    else:
        temp.detail= winner.detail
        del play[(p1,p2)]
        temp2= temp.par
        t1= temp2.p1
        t2= temp2.p2
        play[(t1,t2)]=temp2
        temp.p1=None
        temp.p2=None