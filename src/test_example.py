#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 17:29:54 2019

@author: anita
"""

import vtk
import sys
from math import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import os
import tools2d as tl

#import tools3d as tl3


# Input parameters
AutomaticFile = 'Flowpast_2d_Re3900_v_0.039'
AutomaticVTU_Number = 500
parallel = True
avenum = 1000
linesname = []
U0 = 0.039
p0 = 0.0
rho0 = 1e3
geoname = 'circle.geo'
figurename = 'figure'
bodypoints = 4
xtoD = 1.06



# streamwise velocity U_cl
# with experimental data

# =============================================================================
# x_label = 'x/D'
# y_label = 'U_CL/U_in'
# title = 'Mean streamwise velocity along wake centreline'
# 
# 
# FSs = []
# for i in range(avenum):
#     AutomaticVTU_Number = i
#     a = tl.filters(bodypoints, geoname, AutomaticFile, AutomaticVTU_Number, 
#                  parallel, U0, p0, rho0)
#     detector, FS = a.flowcenterline()
#     FSs.append(FS)
# FS = tl.timeave(np.array(FSs))
# detector, FS = a.modify_relative(detector, FS, mquan = U0)
# 
# b = tl.plotting(detector, FS, x_label, y_label, title, multi = False)
# b.plot_single(figurename, save = False)
# 
# # =============================================================================
# # filename = ['frombelow']
# # xdata, ydata = tl.add_experimental(detector, FS, filename)
# # 
# # 
# # #experimental data
# # filename = '/home/anita/Downloads/experimentdatacsv/u_cl/ex1.csv'
# # x,y = a.experimental(filename)
# # detector.append(x)
# # FS.append(y)
# # 
# # filename = '/home/anita/Downloads/experimentdatacsv/u_cl/ex2.csv'
# # x,y = a.experimental(filename)
# # detector.append(x)
# # FS.append(y)
# # 
# # filename = '/home/anita/Downloads/experimentdatacsv/u_cl/ex3.csv'
# # x,y = a.experimental(filename)
# # detector.append(x)
# # FS.append(y)
# # 
# # filename = '/home/anita/Downloads/experimentdatacsv/u_cl/ex4.csv'
# # x,y = a.experimental(filename)
# # detector.append(x)
# # FS.append(y)
# # 
# # filename = '/home/anita/Downloads/experimentdatacsv/u_cl/ex5.csv'
# # x,y = a.experimental(filename)
# # detector.append(x)
# # FS.append(y)
# # 
# # filename = '/home/anita/Downloads/experimentdatacsv/u_cl/les1.csv'
# # x,y = a.experimental(filename)
# # detector.append(x)
# # FS.append(y)
# # 
# # filename = '/home/anita/Downloads/experimentdatacsv/u_cl/les2.csv'
# # x,y = a.experimental(filename)
# # detector.append(x)
# # FS.append(y)
# # 
# # #plotting
# # b = tl.plotting(detector, FS, x_label, y_label, title, multi = True)
# # b.plot_multi(linesname, figurename, save = False, dot = True)
# # =============================================================================
# =============================================================================




# transverse velocity (6 in wake)

x_label = 'y/D'
y_label = 'u/U_in'
title = 'Transverse profiles of mean streamwise velocity'

#xposition = [0.365, 0.404, 0.452, 0.65, 0.95, 1.25]
xtoD = 1.06

FSs = []
for i in range(avenum):
    AutomaticVTU_Number = i
    a = tl.filters(bodypoints, geoname, AutomaticFile, AutomaticVTU_Number, 
                 parallel, U0, p0, rho0)
    detector, FS = a.waketransverse(xtoD, quanchoose = 1)
    FSs.append(FS)
FS = tl.timeave(np.array(FSs))
detector, FS = a.modify_relative(detector, FS, mquan = U0)

b = tl.plotting(detector, FS, x_label, y_label, title, multi = False)
b.plot_single(figurename, save = False)


# =============================================================================
# filename = ['frombelow']
# xdata, ydata = tl.add_experimental(detector, FS, filename)
# 
# b = tl.plotting(detector, FS, x_label, y_label, title, multi = True)
# b.plot_multi(linesname, figurename, save = False, dot = True)
# =============================================================================



# drag coe Cp

# =============================================================================
# x_label = 'theta'
# y_label = 'Cp'
# title = 'Comparison of the computed surface pressure coefficient distribution'
# 
# FSs = []
# for i in range(avenum):
#     AutomaticVTU_Number = i
#     a = tl.filters(bodypoints, geoname, AutomaticFile, AutomaticVTU_Number, 
#                  parallel, U0, p0, rho0)
#     detector, FS = a.drag_coe_Cp(data_name = 'Pressure')
#     FSs.append(FS)
# FS = tl.timeave(np.array(FSs))
# 
# # Single time
# # =============================================================================
# # a = tl.filters(bodypoints, geoname, AutomaticFile, AutomaticVTU_Number,
# #                parallel, U0, p0, rho0)
# # detector, FS = a.drag_coe_Cp(data_name = 'Pressure')
# # =============================================================================
# 
# b = tl.plotting(detector, FS, x_label, y_label, title, multi = False)
# b.plot_single(figurename, save = False)
# 
# 
# # =============================================================================
# # filename = ['frombelow']
# # xdata, ydata = tl.add_experimental(detector, FS, filename)
# # 
# # b = tl.plotting(detector, FS, x_label, y_label, title, multi = True)
# # b.plot_multi(linesname, figurename, save = False, dot = True)
# # =============================================================================
# =============================================================================
