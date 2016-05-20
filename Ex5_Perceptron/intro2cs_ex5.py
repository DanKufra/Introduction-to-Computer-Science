import matplotlib.pyplot as ploty
import numpy as np


def show_number(A):
    """Plot a matrix to the screen
    Expects A to be a sequence or sequence of sequences (of the same size).
    A should include only numerical values
    Return None"""
    B = np.array(A) 
    ploty.imshow(B,cmap='gray')
    ploty.show()

def loadtxt(filename):
    """ Open and read files for ex5.
    Assumes the file include only numerical values seperated by tabs.
    Each line in filename will be represented as one item in the returned list.
    Such that if the 3rd line included 3 values,
    returned_list[2] will be a list of size 3.
    """
    temp = np.loadtxt(filename,delimiter = '\t')
    return temp.tolist()
    


def show_perceptron(X,Y,w,b):
    """Present the current state of the perceptron algorithm
    where X (seqeunce of sequences) isthe data
    Y - the labels
    w - the candidate seperator
    b- the seprator bias
    Works only for 2D data - X assumed to be sequence of sequences of size 2
    """
    if len(X[0]) != 2 or len(w) != 2:
        print ("Works only for 2d data!")
        return
        

    X = np.array(X)
    Y = np.array(Y)
    w = np.array(w)
    ploty.plot(X[Y==1,0],X[Y==1,1],'bD',markersize=10,linestyle='None',linewidth = 3)
    ploty.plot(X[Y==-1,0],X[Y==-1,1],'ro',markersize=10,linestyle='None',linewidth = 3)
    
    minx = min(X[:,0]) - abs(min(X[:,0]))*0.2
    maxx = max(X[:,0]) + abs(max(X[:,0]))*0.2
    miny = min(X[:,1]) - abs(min(X[:,1]))*0.2
    maxy = max(X[:,1]) + abs(max(X[:,1]))*0.2
    ploty.xlim([minx,maxx])
    ploty.ylim([miny,maxy])
    A = np.arange(minx,maxx,0.01)               
    if w[0] == 0 and w[1] ==0:
        ploty.plot(0,b,'.k',linewidth=2)
        ploty.xlim(min(minx,-0.1),max(maxx,0.1))
        ploty.ylim(min(miny,b-0.1),max(maxy,b+0.1))       
    elif w[1] == 0:
        B = np.arange(miny-abs(miny)*0.2,maxy+abs(maxy)*0.2,0.01)
        b =b/w[0]
        ploty.plot([b]*len(B),B,'k',linewidth=2)
        ploty.xlim(min(minx,b-0.1),max(maxx,b+0.1))
    else:
        l = b/w[1]-(w[0]/w[1])*A
        ploty.plot(A,l,'k',linewidth=2)
        ploty.ylim(min(miny,min(l)),max(maxy,max(l)))
    ploty.show()

