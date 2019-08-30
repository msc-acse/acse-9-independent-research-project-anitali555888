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
#from scipy import interpolate
#from scipy.interpolate import interp1d
#from scipy import integrate
import os



class simulation():
    """
    Modify this class further to integrated with pre-proccessing tools.
    Running the simulation through system command lines.
    
    Attributes:
        binpath: IC-FERST CFD code path (with '/' at the end).
        parallel: Tag for serial or parallel simulations.
        cleanhere: Tag for delete existing vtu/pvtu files.
        npro: For parallel use, the number of proccessors.
            
    Methods:
        run_sim: Run simulations.
    """
    def __init__(self, parallel, codepath, cleanhere = False, npro = None):
        self.codepath = codepath
        self.parallel = parallel
        self.cleanhere = cleanhere
        self.npro = npro
        
        
    def run_sim(self, ):
        """
        Run simulation file mpml.
        """
        # Get paths
        path = os.getcwd()
        binpath = self.codepath + 'bin/icferst'
        #binpath = path[:path.index('legacy_reservoir_prototype')] + 'bin/icferst'
        
        # Remove all vtu files
        if self.cleanhere == True:
            os.system('rm -f ' + path+ '/*.vtu') and os.system('rm -f ' + path+ '/*.pvtu')
        
        # Run all mpml files in serial or parallel
        if self.parallel == False:
            os.system(binpath + ' ' + path + '/*mpml')
        elif self.parallel == True:
            os.system('mpirun' + ' ' + '-n' + ' ' + str(self.npro) + ' ' + binpath 
                      + ' ' + path + '/*mpml')
        return 0


class filters_3d():
    """
    Extract data from one vtu/pvtu file and process.
    
    Attributes:
        bodypoints: Number of points belongs to the bluffy body in geo file.
        geoname: Name of geo file.
        AutomaticFile: Prefix name of vtu/pvtu file.
        AutomaticVTU_Number: Suffix name of vtu/pvtu file.
        parallel: Tag for file extension, from serial or parallel simulations.
        U0: Inlet velocity in stream wise direction.
        p0: Initail presure.
        rho0: Initail density.
        reader: Object with all vtu/pvtu data.
        c0: Coordinates of bluff body center, array with three elements.
        D: Diameter or approximated diameter bluff body.
        geolen: Measurements of geometry, array with three elements.
            
    Methods:
        flowcenterline: Extract data along flow centerline.
        waketransverse: Extracting data along wake transverse.
        drag_coe_Cp: Calculate pressure coefficient.
        modify_relative: Modify data with general value into relative value.
    """
    def __init__(self, bodypoints, geoname, AutomaticFile, AutomaticVTU_Number, 
                 parallel, c0, D, geolen, U0 = None, p0 = None, rho0 = None):
        """
        Read vtu/pvtu file and geo file, set basic information.
        
        """
        self.bodypoints = bodypoints
        self.geoname = geoname
        self.AutomaticFile = AutomaticFile
        self.AutomaticVTU_Number = AutomaticVTU_Number
        self.parallel = parallel
        self.U0 = U0
        self.p0 = p0
        self.rho0 = rho0
        self.c0 = c0
        self.D = D
        self.geolen = geolen
        
        # Reading *.vtu/*.pvtu file
        if (len(sys.argv)>1):
            filename   = sys.argv[1]
            vtu_number = int(sys.argv[2])
        else:
            filename = self.AutomaticFile
            vtu_number = int(self.AutomaticVTU_Number)
        if parallel == True:
            reader = vtk.vtkXMLPUnstructuredGridReader()
            reader.SetFileName(filename+'_'+str(vtu_number)+'.pvtu')
        elif parallel == False:
            reader = vtk.vtkXMLUnstructuredGridReader()
            reader.SetFileName(filename+'_'+str(vtu_number)+'.vtu')
        self.reader = reader
        
# =============================================================================
#         # Read *.geo file
#         info = []
#         infile = open(self.geoname, "rb")
#         for line in infile:
#             if line.split()[0] != 'Point':
#                 break
#             words = line.split('{')[1].split('}')[0].split(', ')
#             
#             nums = []
#             for i in range(3):
#                 num = float(words[i])
#                 nums.append(num)
#             info.append(nums)
#         arrays = np.array(info)
#         
#         self.c0 = arrays[0]
#         r = sum(abs(arrays[1:self.bodypoints + 1, 0] - self.c0[0]))/self.bodypoints 
#         self.D = 2 * r
#         geolen = []
#         for i in range(3):
#             geolen.append(max(arrays[:,i]))
#         self.geolen = np.array(geolen)
# =============================================================================
    
    
    def flowcenterline(self, data_name = 'Velocity', scalar = False, 
                        quanchoose = 0):
        """
        Extracting field data along flow centerline
        :param data_name: field name for extracting
        :param scalar: field type
        :param quanchoose: for vector field (scalar = False), value 0, 1, 2
                            refer to x, y, z
        :return: coordinates and data seperately in array
        """
        ugrid = self.reader.GetOutputPort()
        
        #Initial and last coordinate of the probe
        x0 = self.c0[0] + self.D/2
        x1 = self.geolen[0]
        y0 = self.c0[1]
        y1 = self.c0[1]
        z0 = 0.0
        z1 = self.geolen[2]
        
        # Resolution of the probe
        resolution = 1000
        
        # Create the probe
        hx = (x1 - x0) / resolution
        hy = (y1 - y0) / resolution
        hz = (z1 - z0) / resolution
        
        FS = []
        for i in range(resolution+1):
            detector = []
            for j in range(resolution+1):
                detector.append([hx * i + x0, hy * i + y0, hz * j + z0])
            
            points = vtk.vtkPoints()
            points.SetDataTypeToDouble()
            for j in range(len(detector)):
                points.InsertNextPoint(detector[j][0], detector[j][1], detector[j][2])
            detectors = vtk.vtkPolyData()
            detectors.SetPoints(points)
            probe = vtk.vtkProbeFilter()
            probe.SetInputConnection(ugrid)
            probe.SetSourceConnection(ugrid)
            probe.SetInputData(detectors)
            probe.Update()
            data = probe.GetOutput()
            zFS=[]
            for j in range(points.GetNumberOfPoints()):
                zFS.append(data.GetPointData().GetScalars(data_name).GetTuple(j))
            
            zFS = np.array(zFS)
            fs = []
            for j in range(zFS.shape[1]):
                fs.append(sum(zFS[:, j])/zFS.shape[0])
            FS.append(fs)
        
        # The coordinate along the central line is x
        coordinate = np.array(detector)[:, 0]
        if scalar == True:
            quantity = np.array(FS)[:, 0]
        elif scalar == False:
            quantity = np.array(FS)[:, quanchoose]
        
        return coordinate, quantity
    
    
    def waketransverse(self, xtoD, data_name = 'Velocity', scalar = False, 
                       quanchoose = 0):
        """
        Extracting field data along transverse line in wake
        :param xtoD: Ratio of x to D, x is distance streamwise to 
                        bluff body center
        :param data_name: field name for extracting
        :param scalar: field type
        :param quanchoose: for vector field (scalar = False), value 0, 1, 2
                            refer to x, y, z
        :return: coordinates and data seperately in array
        """
        ugrid = self.reader.GetOutputPort()
        
        #Initial and last coordinate of the probe
        x0 = x1 = xtoD * self.D + self.c0[0]
        y0 = 0.0
        y1 = self.geolen[1]
        z0 = 0.0
        z1 = self.geolen[2]
        
        #Resolution of the probe
        resolution = 1000
        
        #Create the probe
        hx = (x1 - x0) / resolution
        hy = (y1 - y0) / resolution
        hz = (z1 - z0) / resolution
        
        FS = []
        for i in range(resolution+1):
            detector = []
            for j in range(resolution+1):
                detector.append([hx * i + x0, hy * i + y0, hz * j + z0])
            
            points = vtk.vtkPoints()
            points.SetDataTypeToDouble()
            for j in range(len(detector)):
                points.InsertNextPoint(detector[j][0], detector[j][1], detector[j][2])
            detectors = vtk.vtkPolyData()
            detectors.SetPoints(points)
            probe = vtk.vtkProbeFilter()
            probe.SetInputConnection(ugrid)
            probe.SetSourceConnection(ugrid)
            probe.SetInputData(detectors)
            probe.Update()
            data = probe.GetOutput()
            zFS=[]
            for j in range(points.GetNumberOfPoints()):
                zFS.append(data.GetPointData().GetScalars(data_name).GetTuple(j))
            
            zFS = np.array(zFS)
            fs = []
            for j in range(zFS.shape[1]):
                fs.append(sum(zFS[:, j])/zFS.shape[0])
            FS.append(fs)
        
        # The coordinate along the central line is x
        coordinate = np.array(detector)[:, 0]
        if scalar == True:
            quantity = np.array(FS)[:, 0]
        elif scalar == False:
            quantity = np.array(FS)[:, quanchoose]
        
        return coordinate, quantity
    
    
    def drag_coe_Cp(self, data_name = 'Pressure'):
        """
        Calculate pressure coefficient, drag coefficient in pressure 
        distribution method.
        Because rounding of numbers in python, some points in the probe 
        are inside the cylinder, here modify the diameter to avoid that
        (Zoom diameter 101%)
        
        :param data_name: field name for extracting
        :return: theta in degree and Cp seperately in array
        """
        ugrid = self.reader.GetOutputPort()
        self.D = 1.01 * self.D
        # Resolution of the probe
        resolution = 1000
        # Just the upper half of the surface
        delta_theta = np.longfloat(180)/resolution
        z0 = 0.0
        z1 = self.geolen[2]
        
        theta = []
        FS = []
        for i in range(resolution+1):
            theta = []
            detector = []
            theta.append(180 - delta_theta * i)
            x = self.c0[0] + self.D/2 * np.longfloat(cos(radians(180 - delta_theta * i)))
            y = self.c0[1] + self.D/2 * np.longfloat(sin(radians(180 - delta_theta * i)))
            for j in range(resolution+1):
                z = ((z1 - z0) / resolution) * j + z0
                detector.append([x, y, z])
            
            points = vtk.vtkPoints()
            points.SetDataTypeToDouble()
            for j in range(len(detector)):
                points.InsertNextPoint(detector[j][0], detector[j][1], detector[j][2])
            detectors = vtk.vtkPolyData()
            detectors.SetPoints(points)
            probe = vtk.vtkProbeFilter()
            probe.SetInputConnection(ugrid)
            probe.SetSourceConnection(ugrid)
            probe.SetInputData(detectors)
            probe.Update()
            data = probe.GetOutput()
            zFS=[]
            for j in range(points.GetNumberOfPoints()):
                p = data.GetPointData().GetScalars(data_name).GetComponent(j, 0)
                zFS.append((float(p) - self.p0)/(0.5 * self.rho0 * self.U0**2))
            
            zFS = np.array(zFS)
            fs = []
            for j in range(zFS.shape[1]):
                fs.append(sum(zFS[:, j])/zFS.shape[0])
            FS.append(fs)
        
        return np.array(theta), np.array(FS)
    
    
    def modify_relative(self, coordinate, quantity, mquan):
        """
        Modify data with input value into relative ones. After other extracting 
        and calculating methods
        :param coordinate: position value in methods return
        :param quantity: data value in methods return
        :param mquan: value as denominator for quantity
        :return: coordinate and quantity after modification seperately in array
        """
        xdata = coordinate/self.D
        ydata = quantity/mquan
        
        return  xdata, ydata
    

def timeave(ys):
    """
    Function returns data averaged
    :param ys: array with two dimensions
    :return: 
    """
    y = []
    for i in range(ys.shape[1]):
        y.append(sum(ys[:,i])/ys.shape[0])
        
    return np.array(y)


def add_experimental(xdata, ydata, filename, skiprows = 0, delim = ','):
    """
    Read csv files as given a name list, add them with input data in 
    two arrays X, Y and return
    :param xdata: array
    :param ydata: array
    :param filename: filename string or a list of string
    :param skiprows: integer
    :param delim: string
    :return: two arrays
    """
    X = [xdata]
    Y = [ydata]
    if type(filename) is str:
        f = []
        f.append(filename)
    elif type(filename) is list:
        f = filename
    for i in range(len(f)):
        infile = open(f[i], "rb")
        arrays = np.loadtxt(infile, delimiter=delim, skiprows=skiprows)
        X.append(arrays[:,0])
        Y.append(arrays[:,1])
    
    return np.array(X), np.array(Y)


class plotting():
    """
    Plotting functions for line chart. When attributes xdata and ydata are with
    only one index, plot_multi function can not be used. When attributes xdata 
    and ydata are withmore than one index, two plot methods both can be used, 
    just give value of the input msnum of plot_single function.
    
    Attributes:
        xdata: Input array of x coordinate.
        ydata: Input array of y coordinate.
        x_label: Label for x coordinate in string
        y_label: Label for y coordinate in string
        title: Figure title in string.
        multi: Tag for inputs with more than one index.
            
    Methods:
        plot_single: Plot single curve line chart.
        plot_multi: Plot multi curves line chart.
    """
    def __init__(self, xdata, ydata, x_label, y_label, title, multi = False):
        self.xdata = xdata
        self.ydata = ydata
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.multi = multi

 
    def plot_single(self, figurename, msnum = None, save = True):
        """
        Plot single curve in line chart
        :param figurename: filename string, the defalt filetype is 'png' 
                            if no extension here
        :param msnum: index of input arrays
        :param save: tag for save figure
        """
        fig, ax = plt.subplots()
        if self.multi == True:
            x = self.xdata[msnum]
            y = self.ydata[msnum]
        elif self.multi == False:
            x = self.xdata
            y = self.ydata
        
        line = plt.Line2D(x, y)
        ax.add_line(line)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        
        # Autofit figure size in coordinates
        x_min = min(x)-0.1*abs(max(x)-min(x))
        x_max = max(x)+0.1*abs(max(x)-min(x))
        y_min = min(y)-0.1*abs(max(y)-min(y))
        y_max = max(y)+0.1*abs(max(y)-min(y))
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        #plt.show()
        if save == True:
            plt.savefig(figurename)
        
        return 0
    
    
    def plot_multi(self, linesname, figurename, save = True, dot = False):
        """
        Plot multi curves in line chart, when more than 10 curves, line color 
        will keep in grey and marker keeps in Y-like from the 11 line.
        :param linesname: name list of 
        :param figurename: filename string, the defalt filetype is 'png' 
                            if no extension here.
        :param save: tag for save figure
        :param dot: tag for plotting discrete experiemntal data
        """
        fig, ax = plt.subplots()
        X = self.xdata
        Y = self.ydata
        lines=[]
        linestyle=['-']
        color=['r', 'b', 'orange', 'g', 'pink', 'purple', 'k', 'y', 'cyan', 'brown']
        marker=[' ','.','s','v','*','+','x','o','h','p']
        
        x_min = []
        x_max = []
        y_min = []
        y_max = []
        for i in range(X.shape[0]):
            if i >= 10:
                color.append('grey')
            if dot == True:
                linestyle.append(' ')
                marker.append('1')
                line = plt.Line2D(X[i], Y[i], c = color[i], linestyle = 
                                  linestyle[i], marker = marker[i])
            elif dot == False:
                line=plt.Line2D(X[i], Y[i], color=color[i])
            lines.append(line)
            x_min.append(min(X[i])-0.1*abs(max(X[i])-min(X[i])))
            x_max.append(max(X[i])+0.1*abs(max(X[i])-min(X[i])))
            y_min.append(min(Y[i])-0.1*abs(max(Y[i])-min(Y[i])))
            y_max.append(max(Y[i])+0.1*abs(max(Y[i])-min(Y[i])))
        
        for i in range(len(lines)):
            ax.add_line(lines[i])
        
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        
        # Autofit figure size in coordinates
        ax.set_xlim([min(x_min), max(x_max)])
        ax.set_ylim([min(y_min), max(y_max)])
        ax.legend(lines, linesname)
        #plt.show()
        if save == True:
            plt.savefig(figurename)
        
        return 0

