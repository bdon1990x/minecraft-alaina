import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

dim = 30

def plotVoxels(vertices, name):
    fig = plt.figure(figsize=(9,9))
    ax = fig.gca(projection='3d')
    ax.voxels(vertices,edgecolor='k')

    plt.savefig(name)
    
def saveVoxels(dir_name, vox):
    with open(dir_name, 'w') as file:
        for i in range(dim):
            for j in range(dim):
                for k in range(dim):
                    file.write(str(int(vox[i][j][k])))
                    if k == dim - 1:
                        file.write("\n")
                    else:
                        file.write(',')
def loadVoxels(dir_name):
    voxels = np.zeros((dim,dim,dim))
    with open(dir_name) as file:
        for i in range(dim):
            for j in range(dim):
                line = file.readline()
                if line != "":
                    l = np.array(line.split(",")).astype(int)
                    voxels[i][j] = l
    return voxels  
