# My cleanest code
import numpy as np

def window_index(times, dt):

    """
    Returns two lists - forward window f and backward window p defined as follows:
    For each index i in times: 
        f[i] is the smallest index j <= i such that (times[i]-times[j]) <= dt
        p[i] is the largest index k >= i such that (times[k]-times[i]) <= dt
    
    Parameters
    ------------------------
    times: list of of non decreasing times
    dt: time difference
    
    Returns
    -------------------------
    f: list of ints - forward window for each index as above
    p: list of ints - past window for each index as above
    """
    l = len(times)
    f = np.arange(0, l)
    p = np.arange(0, l)
    
    # i is leftmost window, j is rightmost
    i,j = 0,0 
    while (j < l):
        diff = times[j] - times[i]
        if (diff <= dt):
            p[j] = i
            j = j+1
        elif (diff > dt):
            f[i] = (j-1)
            i = i+1
    return p,f

 
def sum_future(values, jump):
    """ Given list of forward window compute sum corresponding to that window for each index """
    totals = [np.sum(values[0:jump[0]+1])]
    for i in range(1, len(values)):
        totals.append(totals[i-1] - values[i-1] + np.sum(values[jump[i-1]+1:jump[i]+1]))
    return totals

   
def sum_past(values, jump):
    """ Given list of backward windows compute sum corresponding to that window for each index """
    l = len(values)-1
    return sum_future(values[::-1], [l-j for j in jump[::-1]])[::-1]


def transform_sum_past(values, times, dt):
    p,f = window_index(times, dt)
    return sum_past(values, p)


# From these three functions we can do lots of things including compute the rolling mean
def rolling_mean_window(values, times, dt):
    p,f = window_index(times, dt)
    return (np.array(sum_future(values,f)) + np.array(sum_past(values, p)) - np.array(values))/(f-p+1)

def rolling_sum(values, times, dt):
    p,f = window_index(times, dt)
    return sum_future(values,f)