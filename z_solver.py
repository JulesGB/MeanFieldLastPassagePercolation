import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.optimize import fsolve
# from scipy.differentiate import derivative

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
    f_bars = np.concatenate((G[:-1], H[::-1]), axis=None) / l
    y = 1 - np.concatenate((G[:-1], H[::-1]), axis=None) / l
    xs = x[1:]
    print(xs)
    print(ys)
    print(f_bars)
    
    ys = np.c_[np.diff(y)/delta]
    # ys = -l * np.diff(y)/delta
    
    return xs, ys, f_bars

def compute_z_pdf_exp(lam, num_samples, high=10):
    func = lambda A: [((A[0])**2 * np.exp(A[0]) / lam) - (2 * np.exp(A[0]) - 2 - A[0])]
    A_lam = fsolve(func, [lam])[0]

    xs = np.linspace(0, high, num_samples)
    z_pdf = lambda x: np.exp(-x) * A_lam / lam
    z_pdf_values = z_pdf(xs)
    z_pdf_values[0] = (1+A_lam) * math.exp(-A_lam)
    print(f'F_delta(0) = {(1+A_lam)*math.exp(-A_lam)}')
    return xs, z_pdf_values, A_lam

    #helper = lambda x: A_lam * np.exp(-x)
    #cdf = lambda x: (1 + helper(x)) / np.exp(helper(x))
    #print(f'cdf(0)={cdf(0)}')
    #
    #xs = np.linspace(0, high, num_samples)
    #delta_pdf = derivative(cdf, xs).df
    #plt.plot(xs, delta_pdf, scaley=False)
    #plt.title('PDF of $\\delta$')
    #print(f'area={integrate.simpson(delta_pdf, x=xs)}')
    #print(f'f_d(0)={delta_pdf[0]}')
    #print(f'f_d(10)={delta_pdf[-1]}')
#
    ## P(Z>x) = exp(-x) * E(exp(-delta))
    ## E(exp(-delta)) = \int_0^{\infty} exp(-x) * f_\delta(x) dx
    #integrand = [math.exp(-x) * delta for x, delta in zip(xs, delta_pdf)]
    #expectation = integrate.simpson(integrand, x=xs)
    #inv_z_cdf = lambda x: np.exp(-x) * expectation
    #print(inv_z_cdf)
#
    #z_xs = np.linspace(-high, high, num_samples * 2)
    #inv_z_pdf = derivative(inv_z_cdf, z_xs).df
    #z_pdf = [-p for p in inv_z_pdf]
    #return z_xs, z_pdf


"""
X = np.linspace(0, .5, N)
x = np.concatenate((X, 0.5+X[1:]), axis=None)
y = 1 - l * np.concatenate((G[:-1], H[::-1]), axis=None)
plt.figure()
plt.plot(x[1:], np.c_[y[1:], np.diff(y)/delta],
         '-', label=['CDF', 'density'])
plt.legend()
"""