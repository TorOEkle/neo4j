
import numpy as np

a = {
    'type': np.array(['house', 'apartment', 'house', 'house', 'terrace-house','terrace-house', 'terrace-house'], dtype='<U13'), 
    'share': np.array([0.5, 0.3, 0.5, 0.5, 0.2, 0.2, 0.2]), 
    'rooms': np.array([3, 3, 3, 4, 3, 3, 1]), 
    'bathrooms': np.array([3, 1, 2, 3, 1, 1, 1]), 
    'size': np.array([180, 110, 149, 103,  51,  55,  91]), 
    'lot_size': np.array([459, 153, 390, 417,   0,   0,   0]), 
    'build_year': np.array([2013, 2013, 1979, 2005, 2003, 2005, 2004]), 
    'people': np.array([6, 3, 4, 1, 2, 1, 1])
    }

addresses = [dict(zip(a, t)) for t in zip(*a.values())]

print(addresses)