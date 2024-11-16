import numpy as np
import matplotlib.pyplot as plt

# compute the cost matrix using the specified metric
def compute_cost_matrix(X, Y, metric='euclidean'):
    X, Y = np.atleast_2d(X, Y)
    
    C = np.zeros((X.shape[1], Y.shape[1]))

    if metric == 'euclidean':
        for i in range(X.shape[1]):
            for j in range(Y.shape[1]):
                C[i, j] = np.sqrt(np.sum((X[:, i] - Y[:, j])**2))  # euclidean distance
    elif metric == 'manhattan':
        for i in range(X.shape[1]):
            for j in range(Y.shape[1]):
                C[i, j] = np.sum(np.abs(X[:, i] - Y[:, j]))  # manhattan distance
    else:
        raise ValueError(f"Unsupported metric: {metric}")
    
    return C

# function to compute the accumulated cost matrix
def compute_accumulated_cost_matrix(C):
    N, M = C.shape
    D = np.zeros((N, M))
    
    # initialize first cell
    D[0, 0] = C[0, 0]
    
    # first column and first row
    for n in range(1, N):
        D[n, 0] = D[n-1, 0] + C[n, 0]
    for m in range(1, M):
        D[0, m] = D[0, m-1] + C[0, m]

    # fill the rest of the matrix
    for n in range(1, N):
        for m in range(1, M):
            D[n, m] = C[n, m] + min(D[n-1, m], D[n, m-1], D[n-1, m-1])

    return D

# function to compute the optimal warping path
def compute_optimal_warping_path(D):
    N, M = D.shape
    n, m = N - 1, M - 1
    path = [(n, m)]
    
    while n > 0 or m > 0:
        if n == 0:
            cell = (0, m - 1)
        elif m == 0:
            cell = (n - 1, 0)
        else:
            # choose the direction with the minimum accumulated cost
            val = min(D[n-1, m-1], D[n-1, m], D[n, m-1])
            if val == D[n-1, m-1]:
                cell = (n-1, m-1)
            elif val == D[n-1, m]:
                cell = (n-1, m)
            else:
                cell = (n, m-1)
        
        path.append(cell)
        n, m = cell
    
    path.reverse()
    return np.array(path)

# example usage

X = np.array([1, 2, 3, 4, 5])
Y = np.array([1, 3, 4, 6, 5])

# step 1: compute the cost matrix between X and Y using Euclidean distance
C = compute_cost_matrix(X, Y, metric='euclidean')
print('Cost matrix C:')
print(C)

# step 2: compute the accumulated cost matrix from the cost matrix
D = compute_accumulated_cost_matrix(C)
print('\nAccumulated cost matrix D:')
print(D)

# step 3: compute the optimal warping path
P = compute_optimal_warping_path(D)
print('\nOptimal warping path P:')
print(P)

# step 4: display the results graphically
plt.figure(figsize=(8, 6))

# plot the sequences
plt.subplot(2, 1, 1)
plt.plot(X, label='Sequence X')
plt.plot(Y, label='Sequence Y')
plt.title('Sequences X and Y')
plt.legend()

# plot the DTW warping path
plt.subplot(2, 1, 2)
plt.imshow(D, cmap='Blues', interpolation='nearest')
plt.plot(P[:, 1], P[:, 0], color='r', marker='o', linestyle='-', markersize=6)
plt.title('DTW Accumulated Cost Matrix with Optimal Warping Path')
plt.colorbar()

plt.tight_layout()
plt.show()

# Final DTW distance
print(f'\nDTW distance between X and Y: {D[-1, -1]}')
