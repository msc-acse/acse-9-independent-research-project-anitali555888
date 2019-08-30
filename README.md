# ACSE-9 Independent Research Project

## Integration of CFD Modelling Framework IC-FERST for Industrial Application in BP: Automation of pre- and post-processing using Python

## Author and Course Information

Author：Dongzhen Li

Github alias: anitali555888

Email: dongzhen.li18@imperial.ac.uk

Supervisor/Advisor: Asiri Obeysekara, Andre Nicolle, Chris Pain

## Introduction
From the engineeing motivation to a review of flow past a cylinder, and finally to the development of a practical post-processing tool for cases relevant to the classic ideal case flow past a cylinder for integration purposes with IC-FERST, this project introduce the implementation details and the physical background. Some generalisation implementation from flow past cylinder is explained in this report, and the future modification possibility is discussed as well. IC-FERST is a CFD solver based on Fluidity for solving Navier-Stokes equations in 2 and 3 dimensions developed in AMCG Imerial College London. It is a general-purpose code for simulating multiphase flow and transport in complex geological reservoirs. This project is related to a research project between Imperial College and BP to evaluate IC-FERST. 

picture


## Installation and Requirements:
### Requirements:
   - Python (2.7) as well as:
        - Numpy
        - Matplotlib
        - Pytest
   - IC-FERST http://multifluids.github.io/license/
   - vtk https://www.vtk.org/doc/nightly/html/pages.html
   
Afer ensuring that those requirements are installed securely, creating a python .py file with scripts as the test_example.py in the scr folder under the same location with simulation files (.geo, .msh, .mpml) and running it to the expected output.

## Documentation

The documentation of code here is based in the report and the code comments.

## Run test cases

- Flow past cylinder 2D & 3D :

In the folder test cases/, the two folder are for FPC 2D and 3D model tests. Simplyly call the file 2d_test_example.py and 3d_test_example.py to test.


## tools2d.py and tools3d.py:

Instructure of these two module in folder src/.

```python
class simulation: Runing simulation.

class filters: Filters in functions to analyse data.

class plotting: Create pictures.

# Two functions to help implementation of filters.
def timeave():

def add_experimental():
```

## Example figures:

In the pic folder.

## License
This project is licensed by [MIT](https://choosealicense.com/licenses/mit/).
