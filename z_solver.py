import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.differentiate import derivative

def A(data):
    return [(1+x) * np.exp(-x) for x in data]

def transform(G, H, l, delta):
    H1 = np.cumsum(A(G)) * delta * l
    H1 = H1 - H1[0]
    G1 = -1 * np.cumsum(A(H1)) * delta * l
    G1 = G1 - G1[-1] + H1[-1]
    return G1, H1

# N = num_samples
def compute_z_pdf(l, num_samples, num_iterations=20, print_iters=False):
    delta = 0.5 / num_samples # delta = 0.5/N for numerical integration
    H = np.zeros(num_samples)
    G = -1 * np.cumsum(A(H)) * delta * l
    G = G - G[-1] + H[-1]
    
    for i in range(num_iterations): # 20 iterations, increase if needed
        G, H = transform(G, H, l, delta)
        if print_iters:
            print('Iteration = %2d, Mass at 0 = %10.9f' % (i+1, 1-l * G[0]))

    X = np.linspace(0, .5, num_samples)
    x = np.concatenate((X, 0.5+X[1:]), axis=None)
    y = 1 - np.concatenate((G[:-1], H[::-1]), axis=None) / l
    xs = x[1:]
    
    ys = np.c_[np.diff(y)/delta]
    # ys = -l * np.diff(y)/delta
    
    return xs, ys

def compute_z_pdf_exp(lam, num_samples):
    func = lambda A: [A[0]**2 * np.exp(A[0]) / lam - (2 * np.exp(A[0]) - 2 - A[0])]
    A_lam = fsolve(func, [lam])[0]

    helper = lambda x: A_lam * np.exp(-x)
    #cdf = lambda x: (1 + helper(x[0])) * np.exp(-1 * helper(x[0]))
    cdf = lambda x: (1 + helper(x)) * np.exp(-1 * helper(x))
    
    xs = np.linspace(0, 1, num_samples)
    ys = [cdf(x) for x in xs]
    #pdf = derivative(cdf, xs, preserve_shape=True)
    #return pdf.df
    pdf = np.diff(ys) * num_samples # (f(x+1) - f(x)) / h, h = (1-0)/num_samples
    return pdf


"""
X = np.linspace(0, .5, N)
x = np.concatenate((X, 0.5+X[1:]), axis=None)
y = 1 - l * np.concatenate((G[:-1], H[::-1]), axis=None)
plt.figure()
plt.plot(x[1:], np.c_[y[1:], np.diff(y)/delta],
         '-', label=['CDF', 'density'])
plt.legend()
"""