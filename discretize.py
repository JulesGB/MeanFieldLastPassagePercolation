import math
from scipy.stats import binned_statistic

def discretize_linear(data, num_bins, low=None, high=None):   
    if low is None:
        low = data.min()
    if high is None:
        high = data.max()
        
    return binned_statistic(data, None,
                            statistic='count',
                            bins=num_bins, range=(low,high))

# Take a list of data with points in [0, +inf) and split into log bins
def discretize_log(data, num_bins):
    bins = []
    for i in range(num_bins, 1, -1):
        # -log(i/k) = log(k) - log(i)
        bins.append(math.log(num_bins) - math.log(i))
    bins.append(float("inf"))
    
    return binned_statistic(data, None,
                            statistic='count',
                            bins=bins, range=(0.0, float("inf")))