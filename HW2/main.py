import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

n = 20  # number of vertices
adj = np.zeros([n,n])   # 0: uncolored  1: black  -1: white

def cal_black(adj,i,j,k,l):
    # color (i,j) with black
    color_array = np.array([adj[i,k],adj[i,l],adj[j,k],adj[j,l],adj[k,l]])

    if -1 in color_array:
        return 0
    else:
        r = (color_array==1).sum()

    return 2**float(r-5)

def cal_prev(adj,i,j,k,l):
    # (i,j) uncolored
    color_array = np.array([adj[i,k],adj[i,l],adj[j,k],adj[j,l],adj[k,l]])

    if (1 in color_array) and (-1 in color_array):
        return 0
    elif 1 in color_array:
        r = (color_array==1).sum()
        return 2**float(r-6)
    elif -1 in color_array:
        r = (color_array==-1).sum()
        return 2**float(r-6)
    else:
        return 2**(-5)

        

W = n*(n-1)*(n-2)*(n-3)/(24*32) # init W
W_list = [W]

for i in tqdm(range(n)):
    for j in range(i+1,n):
        # coloring (i,j) with black
        W_black = W
        other_vertices = list(range(0,i))+list(range(i+1,j))+list(range(j+1,n))

        for k_ind in range(len(other_vertices)):
            for l_ind in range(k_ind+1,len(other_vertices)):
                k = other_vertices[k_ind]
                l = other_vertices[l_ind]
                # K4 (i,j,k,l) with (i,j) black
                W_black += ( cal_black(adj,i,j,k,l) - cal_prev(adj,i,j,k,l) )
        # print(i,j,"W_black=",W_black)

        if W_black < W:
            # color (i,j) with black
            adj[i,j] = 1
            adj[j,i] = 1
            W = W_black
            # print(i,j,"W_black=",W_black,"black")
        else:
            # color (i,j) with white
            adj[i,j] = -1
            adj[j,i] = -1
            W = 2*W - W_black
            # print(i,j,"W_black=",W_black,"white")

        W_list.append(W)

print("Expectation:",W_list[0])
print("Algr. Result:",W_list[-1])
plt.plot(W_list)
plt.title("Number of homochrome K4, n="+str(n))
plt.savefig(fname = "./figs/n="+str(n))
plt.show()
