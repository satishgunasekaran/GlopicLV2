# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 00:59:12 2020

@author: hp
"""

from itertools import combinations_with_replacement
from collections import defaultdict

import numpy as np
from numpy.linalg import inv

B, G, R = 0, 1, 2  

def boxfilter(I, r):
    """Fast box filter implementation.
    Parameters
    ----------
    I:  a single channel/gray image data normalized to [0.0, 1.0]
    r:  window radius
    Return
    -----------
    The filtered image data.
    """
    M, N = I.shape
    dest = np.zeros((M, N))
   
    
   
    sumY = np.cumsum(I, axis=0)
    
    dest[:r + 1] = sumY[r:2*r + 1] 
    dest[r + 1:M - r] = sumY[2*r + 1:] - sumY[:M - 2*r - 1]
    
    dest[-r:] = np.tile(sumY[-1], (r, 1)) - sumY[M - 2*r - 1:M - r - 1] 

    
    sumX = np.cumsum(dest, axis=1)
    
    dest[:, :r + 1] = sumX[:, r:2*r + 1] 
    dest[:, r + 1:N - r] = sumX[:, 2*r + 1:] - sumX[:, :N - 2*r - 1]
    dest[:, -r:] = np.tile(sumX[:, -1][:, None], (1, r)) - sumX[:, N - 2*r - 1:N - r - 1] 

  

    return dest


def guided_filter(I, p, r=15, eps=1e-3):
    """Refine a filter under the guidance of another (RGB) image.
    Parameters
    -----------
    I:   an M * N * 3 RGB image for guidance.
    p:   the M * N filter to be guided. transmission is used for this case.
    r:   the radius of the guidance
    eps: epsilon for the guided filter
    Return
    -----------
    The guided filter.
    """
    M, N = p.shape
    base = boxfilter(np.ones((M, N)), r)
    
    
    means = [boxfilter(I[:, :, i], r) / base for i in range(3)]
    
  
    mean_p = boxfilter(p, r) / base

  
    means_IP = [boxfilter(I[:, :, i]*p, r) / base for i in range(3)]

  
    covIP = [means_IP[i] - means[i]*mean_p for i in range(3)]

    
    var = defaultdict(dict)
    for i, j in combinations_with_replacement(range(3), 2):
        var[i][j] = boxfilter(I[:, :, i]*I[:, :, j], r) / base - means[i]*means[j]

    a = np.zeros((M, N, 3))
    for y, x in np.ndindex(M, N):
        
        Sigma = np.array([[var[B][B][y, x], var[B][G][y, x], var[B][R][y, x]],
                          [var[B][G][y, x], var[G][G][y, x], var[G][R][y, x]],
                          [var[B][R][y, x], var[G][R][y, x], var[R][R][y, x]]])
        cov = np.array([c[y, x] for c in covIP])
        a[y, x] = np.dot(cov, inv(Sigma + eps*np.eye(3)))  # eq 14

   
    b = mean_p - a[:, :, R]*means[R] - a[:, :, G]*means[G] - a[:, :, B]*means[B]

  
    q = (boxfilter(a[:, :, R], r)*I[:, :, R] + boxfilter(a[:, :, G], r)*I[:, :, G] + boxfilter(a[:, :, B], r)*I[:, :, B] + boxfilter(b, r)) / base

    return q
