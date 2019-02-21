# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 14:35:51 2018

@author: jackyrj
"""


import numpy as np

def R2_fun(y, y_forecast, testing):
    # 拟合优度R^2
    y_mean=np.mean(y[-testing:])
    return 1 - (np.sum((y_forecast[-testing:] - y[-testing:]) ** 2)) / (np.sum((y[-testing:] - y_mean) ** 2))

#def E_fun(y, y_forecast, testing, error_power, k, error_epsilon):
#    # 拟合度E
#    y_mean=np.mean(y)
#    y_e = np.abs(y[-testing:] - y_forecast[-testing:]) / (np.abs(y[-testing:] - y_mean)  + error_epsilon) 
#    y_sum = k * np.sum((y_e) ** error_power) / testing + 1
#    return 1 - ((y_sum) ** (1 / error_power) - 1) / (1 + (y_sum) ** (1 / error_power))

#def E2_fun(y, y_forecast, testing, error_power):
#    # 拟合度E
#    y_e = np.abs(y[-testing:] - y_forecast[-testing:]) / (np.abs(y[-testing:] - np.mean(y[-testing:])) + 10**-10) 
#    y_sum = np.sum((y_e) ** error_power) / testing + 1
#    a=((y_sum) ** (1 / error_power) - 1)
#    b =  (1 + (y_sum) ** (1 / error_power))
##    return 1 - (np.exp(y_sum) ** (1 / error_power) - 1) / (1 + np.exp(y_sum) ** (1 / error_power))
#    return 1- a / b
#    
#def error_fun8(y, y_forecast, testing, error_power, error_k, error_epsilon):
#    # 拟合度E
#    y_mean = np.mean(y[-testing:])
#    y_e = np.abs(y[-testing:] - y_forecast[-testing:]) / (np.abs(y[-testing:] - y_mean)  + error_epsilon) 
#    y_sum = error_k * np.sum((y_e) ** error_power) / testing + 1
#    return  ((y_sum) ** (1 / error_power) - 1) / (1 + (y_sum) ** (1 / error_power)) 

def E_fun(y, y_forecast, testing, error_power, error_k, error_epsilon):
    # 拟合度E
    y_mean=np.mean(y[-testing:])
    z = (np.sum((abs(y_forecast[-testing:] - y[-testing:])) ** error_power)) / (np.sum((abs(y[-testing:] - y_mean)) ** error_power) + error_epsilon) * error_k
    return 1 / (1 + (z) ** (1 / error_power))

import matplotlib.pyplot as plt

n= 1000
b = 10
c = 100
A = np.linspace(0.5, 1.5, n)
error_power = 2
k = 1
error_epsilon = 2 ** -50

x = np.linspace(0, 1, n)
y = np.sin(x) * b + c
y_forecast = [A[i] * np.sin(x) * b + c for i in range(n)]

R2 = [R2_fun(y, y_forecast[i], n) for i in range(n)]
E = [E_fun(y, y_forecast[i], n, error_power, k, error_epsilon) for i in range(n)]

fig= plt.figure()
plt.plot(A, R2, 'r')
plt.plot(A, E, 'b')


A = np.linspace(-10, 10, n)
y_forecast = [A[i] * np.sin(x) * b + c for i in range(n)]
E = [E_fun(y, y_forecast[i], n, error_power, k, error_epsilon) for i in range(n)]

fig= plt.figure()
plt.plot(A, E, 'b')


