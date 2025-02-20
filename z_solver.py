import numpy as np
import matplotlib.pyplot as plt

def A(data):
    return [(1+x) * np.exp(-x) for x in data]

def transform(G, H, lam, delta):
    H1 = np.cumsum(A(G)) * delta/lam
    H1 = H1 - H1[0]
    G1 = -1 * np.cumsum(A(H1)) * delta/lam
    G1 = G1 - G1[-1] + H1[-1]
    return G1, H1

# N = num_samples
def compute_z_pdf(lam, num_samples, num_iterations=20, print_iters=False):
    delta = 0.5 / num_samples # delta = 0.5/N for numerical integration
    H = np.zeros(num_samples)
    G = -1 * np.cumsum(A(H)) * delta/lam
    G = G - G[-1] + H[-1]
    
    for i in range(num_iterations): # 20 iterations, increase if needed
        G, H = transform(G, H, lam, delta)
        if print_iters:
            print('Iteration = %2d, Mass at 0 = %10.9f' % (i+1, 1-lam * G[0]))

    X = np.linspace(0, .5, num_samples)
    x = np.concatenate((X, 0.5+X[1:]), axis=None)
    y = 1 - lam * np.concatenate((G[:-1], H[::-1]), axis=None)
    xs = x[1:]
    ys = np.c_[y[1:], np.diff(y)/delta]
    
    #plt.figure()
    #plt.plot(xs, ys, '-', label=['CDF', 'density'])
    #plt.legend()
    
    return xs, ys

"""
X = np.linspace(0, .5, N)
x = np.concatenate((X, 0.5+X[1:]), axis=None)
y = 1 - l * np.concatenate((G[:-1], H[::-1]), axis=None)
plt.figure()
plt.plot(x[1:], np.c_[y[1:], np.diff(y)/delta],
         '-', label=['CDF', 'density'])
plt.legend()
"""