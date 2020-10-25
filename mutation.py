import random

def is_good_perm2(lst):
  	return sorted(lst) == list(range(1, len(lst) + 1))

#mutations for such as neighbor switch or swap
def mutation_rand_swap(perm, mutation_rate):
    perm_len = len(perm)
    for i in range(perm_len):
        chance = random.uniform(0,1)
        if chance < mutation_rate:
            j = random.randrange(perm_len)
            perm[i], perm[j] = perm[j], perm[i]
			

def mutation_neigh_swap(perm, mutation_rate):
    assert is_good_perm2(perm)
    perm_len = len(perm)
    for i in range(perm_len-1):
        chance = random.uniform(0,1)
        if chance<mutation_rate:
            temp = perm[i]
            perm[i] = perm[i+1]
            perm[i+1] = temp

def mutation_section_shuffle(perm, mutation_rate):
    assert is_good_perm2(perm)
    chance = random.uniform(0,1)
    if chance>mutation_rate:
        return 

    perm_len = len(perm)
    A = random.randint(0,perm_len-2)
    B = random.randint(A+1, perm_len)
    temp = perm[A:B]
    random.shuffle(temp)
    St1 = 0
    for i in range(A,B):
        perm[i] = temp[St1]
        St1+=1
    assert is_good_perm2(perm)


#https://www.researchgate.net/publication/282732991_A_New_Mutation_Operator_for_Solving_an_NP-Complete_Problem_Travelling_Salesman_Problem
def mutation_RSM(perm, mutation_rate):
    assert is_good_perm2(perm)
    chance = random.uniform(0,1)
    if chance>mutation_rate:
        return 
    perm_len = len(perm)

    A = random.randint(0,perm_len-2)
    B = random.randint(A+1, perm_len-1)
    while A < B:
        temp = perm[A]
        perm[A] = perm[B]
        perm[B] = temp
        A+=1
        B-=1

def mutation_RSM_neigh_swap(perm, mutation_rate):
    assert is_good_perm2(perm)

    chance = random.uniform(0,1)
    if chance > mutation_rate:
        return 
    perm_len = len(perm)
    A = random.randint(0,perm_len-2)
    B = random.randint(A+1, perm_len-1)
    while (A<B):
        temp = perm[A]
        perm[A] = perm[B]
        perm[B] = temp
        chance = random.uniform(0,1)
        if chance < mutation_rate:
            temp = perm[A]
            perm[A] = perm[A+1]
            perm[A+1] = temp
        A+=1
        B-=1

def converge_X(permA, permB):
    assert is_good_perm2(permA)
    assert is_good_perm2(permB)
    #copy identical of the two perms and fill the rest with randoms
    child = []
    pos = []
    missing  = []
    perm_len = len(permA)
    for i in range(perm_len):
        if permA[i]==permB[i]:
            child.append(permA[i])
        else:
            child.append(-1)
            missing.append(permA[i])
            pos.append(i)

    pos_len  = len(pos)
    for j in range(pos_len):
        mychoice = random.randint(0,pos_len - j-1)
        child[ pos[j] ] = missing[mychoice]
        del missing[mychoice]
    assert is_good_perm2(child)
    return child

def OX(permA, permB):
    perm_len = len(permA)
    A = random.randint(0,perm_len-2)
    B = random.randint(A+1, perm_len-1)
    # A = 3
    # B = 7
    child1 = [-1] * perm_len
    child2 = [-1] * perm_len
    #copy item between segment
    for i in range(A,B):
        child1[i]=permA[i]
        child2[i] =permB[i]
    j1 = B
    j2 = B
    j3 = B
    flag1 = False
    flag2 = False 
    while not (j2==B and flag1==True and flag2==True):
        if j2==perm_len:
            j2 = 0
        if j1==perm_len:
            j1 = 0
            flag1 = True
        if j3==perm_len:
            j3 = 0
            flag2 = True
        if permB[j2] not in child1:
            child1[j1] = permB[j2]
            j1+=1
        if permA[j2] not in child2:
            child2[j3] =  permA[j2]
            j3+=1
        # print(f"j1 = {j1} j3 = {j3} j2 = {j2}")
        j2+=1
    assert is_good_perm2(child1)
    assert is_good_perm2(child2)
    return child1, child2



def CX2(permA, permB): #https://www.hindawi.com/journals/cin/2017/7430125/
    child1 = []
    child2 = []
    St1 = 0
    St2 = 0 
    #step2 select 1st bit from other 2nd parent
    child1.append(permB[St1])
    #step3
    N = len(permA)
    while St1 <N:
        pos = permA.index(child1[St1])
        val = permB[pos]
        pos = permA.index(val)
        val = permB[pos]
        child2.append(val)
        if val==permA[St2]:
            #find the first val in permA that isn't in child1
            for i in range(St2,N):
                if permB[i] not in child1:
                    pos = i
                    St2 = i
                    break
        else:
            pos = permA.index(val)
        St1+=1
        if (St1>N-1):
            break
        val = permB[pos]
        child1.append(val)
    assert(is_good_perm2(child1))
    assert(is_good_perm2(child2))
    return child1, child2
    
def main():
    # p1 = [3,4,8,2,7,1,6,5]
    # p2 = [4,2,5,1,6,8,3,7]
    p1 = [1,2,3,4,5,6,7,8]
    p2 = [2,7,5,8,4,1,6,3]
    p1,p2 = CX2(p1, p2)
    print(p1)
    print(p2)

main()