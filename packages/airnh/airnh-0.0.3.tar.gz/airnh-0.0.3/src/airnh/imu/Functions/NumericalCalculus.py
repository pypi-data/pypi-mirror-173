import numpy as np

'''
@params data: N x M matrix, where N is number of data, M is the columns
@params ts: N x 1 matrix, where N is number of data, and with time stamp
'''
def derivative(data, ts):
    dt_array = ts[1:] - ts[:-1]
    return (data[1:] - data[:-1])/dt_array


'''
@params data: N x M matrix, where N is number of data, M is the columns
@params ts: N x 1 matrix, where N is number of data, and with time stamp
'''
def integrate(data, ts):
    N = data.shape[0]
    dt_array = ts[1:] - ts[:-1]
    result = np.zeros_like(data)
    for i in range(0, N-1):
        row = data[i]
        dt = dt_array[i]
        result[i+1] = result[i] + row*dt
    return result
