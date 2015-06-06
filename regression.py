import numpy as np
y = [-6,-5,-10,-5,-8,-3,-6,-8,-8]
x = [
        [-4.95,-4.55,-10.96,-1.08,-6.52,-0.81,-7.01,-4.46,-11.54],
        [-5.87,-4.52,-11.64,-3.36,-7.45,-2.36,-7.33,-7.65,-10.03],
        [-0.76,-0.71,-0.98,0.75,-0.86,-0.50,-0.33,-0.94,-1.03],
        [14.73,13.74,15.49,24.72,16.59,22.44,13.93,11.40,18.18],
        [4.02,4.47,4.18,4.96,4.29,4.81,4.32,4.43,4.28],
        [0.20,0.16,0.19,0.16,0.10,0.15,0.21,0.16,0.21],
        [0.45,0.50,0.53,0.60,0.48,0.53,0.50,0.49,0.55]
    ]
    
X = np.column_stack(x+[[1]*len(x[0])])

beta_hat = np.linalg.lstsq(X,y)[0]

print beta_hat

# from numpy import *
# x = array([0,1,2,3,4,5])
# y = array([0,0.8,0.9,0.1,-0.8,-1])
# print(x)
# print(y)
#
# from scipy.interpolate import *
# p1 = polyfit(x,y,1)
# p2 = polyfit(x,y,2)
# p3 = polyfit(x,y,3)
# print(p1)
# print(p2)
# print(p3)
#
# from matplotlib.pyplot import *
# plot(x,y,'o')
# xp = linspace(-2,6,100)
# plot(xp,polyval(p1,xp),'r-')
# plot(xp,polyval(p2,xp),'b--')
# plot(xp,polyval(p3,xp),'m:')
# yfit = p1[0] * x + p1[1]
# yresid= y - yfit
# SSresid = sum(pow(yresid,2))
# SStotal = len(y) * var(y)
# rsq = 1 - SSresid/SStotal
# print(yfit)
# print(y)
# print(rsq)
#
# from scipy.stats import *
# slope,intercept,r_value,p_value,std_err = linregress(x,y)
# print(pow(r_value,2))
# print(p_value)
# show()

import numpy as np

from matplotlib.pyplot import *

# x = np.array([1, 2, 3, 4, 5])

x = np.array([[1, 2, 3,4,5], [4, 5, 6,7,8], [41, 8, 16,27,18]])

y = np.array([2, 3, 4, 4, 5])

n = np.max(x.shape)

X = np.vstack([np.ones(n), x]).T


a = np.linalg.lstsq(X, y)[0]

print a

