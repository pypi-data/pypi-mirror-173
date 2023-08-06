#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/29 19:36
# @Author  : Zhou Huajun
# @File    : test_base_data.py
# @Contact : 17601244133@163.com
# @From    : Tongji University

import pandas as pd
import numpy as np

class HolderTable:
    def __init__(self,sut=None):
        self.scenario_shape = 2

    def test(self,sample,sut=None,metric=None):
        scenario = scenario.reshape(-1,self.scenario_shape)
        sample = np.array(sample)
        x1 = sample[:,0]
        x2 = sample[:,1]
        ex_up = np.abs(1-np.sqrt(x1**2+x2**2)/np.pi)
        y = np.abs(np.sin(x1)*np.cos(x2)*np.exp(ex_up))-5
        return y

class ENV(HolderTable):
    pass

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    upper_bound = np.array([10,10])
    lower_bound = np.array([-10,-10])
    print(upper_bound, lower_bound)
    linsp = np.array([0.5, 0.5])
    grad = []
    for i in range(upper_bound.shape[0]):
        grad += [np.arange(lower_bound[i], upper_bound[i], linsp[i])]
    a = np.meshgrid(*grad)
    x_all = np.vstack([x.ravel() for x in a]).T
    Xp,Yp = np.meshgrid(*grad)
    print(x_all.shape,Xp.shape,Yp.shape)

    env = ENV()
    res = env.test(x_all)

    # 绘图
    fig = plt.figure()
    ax1 = plt.axes(projection='3d')
    ax1.plot_surface(Xp, Yp, res.reshape(Xp.shape[0],-1),rstride=1, cstride=1,cmap='viridis', edgecolor='none')
    plt.show()