import math
#from numpy import linspace
from scipy.stats import *

# Generates bin edges for log discretization
def log_bins(num_bins):
    num_bins += 1
    #bins = [float("-inf")]
    bins = []
    #for i in range(2, num_bins):
    #    bins.append(-1 * (math.log(num_bins) - math.log(i)))
    for i in range(num_bins, 1, -1):
        # -log(i/k) = log(k) - log(i)
        bins.append(math.log(num_bins) - math.log(i))
    bins.append(float("inf"))
    #print(bins)
    return bins

def discretize_linear(data, num_bins, low=None, high=None):   
    if low is None:
        low = data.min()
    if high is None:
        high = data.max()
        
    return binned_statistic(data, None,
                            statistic='count',
                            bins=num_bins, range=(low,high))

def discretize_linear_2d(data, num_bins, low=0, high=1):   
    x, y = [*zip(*data)]
    #bins = linspace(low, high, num_bins)
    return binned_statistic_2d(x, y, None, bins=num_bins,
                               statistic='count',
                               range=((low,high), (low,high)))
    

# Take a list of data with points in [0, +inf) and split into log bins
def discretize_log(data, num_bins):
    bins = log_bins(num_bins)
    return binned_statistic(data, None,
                            statistic='count',
                            bins=bins, range=(0.0, float("inf")))

def discretize_log_2d(data, num_bins):
    bins = log_bins(num_bins)
    x, y = [*zip(*data)]
    return binned_statistic_2d(x, y, None,
                               statistic='count', bins=bins,
                               range=((0.0,float('inf')), (0.0,float('inf'))))

