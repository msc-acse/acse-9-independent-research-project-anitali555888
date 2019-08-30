#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Dongzhen Li

Github alias: anitali555888

"""

import vtk
import sys
from math import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import os
from src import tools2d as tl

AutomaticFile = 'Flowpast_2d_Re3900_v_0.039'
AutomaticVTU_Number = 500
U0 = 0.039
p0 = 0.0
rho0 = 1e3
geoname = 'circle.geo'
figurename = 'pytest'
filename = '/path to csv/'
bodypoints = 4
xtoD = 1.06


def test_flowcenterline():
    """
    Test the function of centerline data extraction.
    """
    f = tl.filter(bodypoints, geoname, AutomaticFile, AutomaticVTU_Number, 
                 parallel = True, U0, p0, rho0)
    x, y = f.flowcenterline()
    assert(y.shape[1] == 1001)
    print 'Centerline data extraction works.'


def test_waketransverse():
    """
    Test the function of transverse at wake data extraction.
    """
    f = tl.filter(bodypoints, geoname, AutomaticFile, AutomaticVTU_Number, 
                 parallel = True, U0, p0, rho0)
    x, y = f.waketransverse(xtoD, quanchoose = 0)
    assert(y.shape[1] == 1001)
    print 'Transverse at wake data extraction works.'


def test_drag_coe_Cp():
    """
    Test the function of drag coe Cp.
    """
    f = tl.filter(bodypoints, geoname, AutomaticFile, AutomaticVTU_Number, 
                 parallel = True, U0, p0, rho0)
    x, y = f.drag_coe_Cp()
    assert(y.shape[1] == 1001)
    print 'Draf coe calculation works.'


def test_modify_relative():
    """
    Test the function of data relative modification.
    """
    f = tl.filter(bodypoints, geoname, AutomaticFile, AutomaticVTU_Number, 
                 parallel = True, U0, p0, rho0)
    x = np.array([1,2,3,4,5,6,7,8,9])
    y = np.array([1,2,3,4,5,6,7,8,9])
    a, b = f.modify_relative(x, y, 2)
    assert(b[1] == 1))
    print 'Relative data is OK.'


def test_timeave():
    """
    Test the function of running simulation.
    """
    x = np.array([1,2,3,4,5,6,7,8,9])
    y = np.array([x,x])
    a = timeave(y)
    assert(a == np.array([1,2,3,4,5,6,7,8,9]))
    print 'Time averaging tool works OK.'
    

def test_add_experimental():
    """
    Test the function of running simulation.
    """
    x = np.array([1,2,3,4,5,6,7,8,9])
    y = np.array([1,2,3,4,5,6,7,8,9])
    a, b = tl.add_experimental(x, y, filename)
    assert(a[1] == np.array([9,9,9]))
    print 'Experimental data added.'


def test_plot_single():
    """
    Test the function of creating single-line figure.
    """
    x = np.array([1,2,3,4,5,6,7,8,9])
    y = np.array([1,2,3,4,5,6,7,8,9])
    p = tl.plotting(x, y)
    assert(p.plot_single(figurename) == 0)
    print 'Single-line figure OK.'


def test_plot_multi():
    """
    Test the function of creating multi-line figure.
    """
    x = np.array([1,2,3,4,5,6,7,8,9]).reshape(3,3)
    y = np.array([1,2,3,4,5,6,7,8,9]).reshape(3,3)
    p = tl.plotting(x, y, multi = False)
    assert(p.plot_multi(figurename) == 0)
    print 'Multi-line figure OK.'