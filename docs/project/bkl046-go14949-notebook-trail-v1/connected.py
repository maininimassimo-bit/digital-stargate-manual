import numpy as np


def connected(mask, seeds):
    result=np.zeros(mask.shape,dtype=bool)
    height,width=mask.shape
    pending=[tuple(map(int, point)) for point in np.argwhere(seeds)]
    for y,x in pending:
        result[y,x]=True
    while pending:
        y,x=pending.pop()
        for i in range(max(0,y-1),min(height,y+2)):
            for j in range(max(0,x-1),min(width,x+2)):
                if mask[i,j] and not result[i,j]:
                    result[i,j]=True
                    pending.append((i,j))
    return result