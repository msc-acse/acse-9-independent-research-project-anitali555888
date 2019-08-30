# ACSE-9 Independent Research Project

## Integration of CFD Modelling Framework IC-FERST for Industrial Application in BP:
## Automation of pre- and post-processing using Python

### Dongzhen Li

### Supervisor/Advisor: Asiri Obeysekara, Andre Nicolle, Chris Pain
### Github alias: anitali555888\\
### Email: dongzhen.li18@imperial.ac.uk}

## Installation and Requirements:
### Requirements:
   - Python 3.6 standard library as well as:
        - Numpy
        - Scipy
        - Matplotlib
        - Pytest
        - Mpl_toolkits
   - Jupyter notebook (Included in Anaconda)
   - IPython Kernel   (Included in Anaconda)
   
Simply ensure that the above required libraries and software is installed, and then clone the repository locally. All data files are included.

## tools2d.py:

Classes of functions in this module.

```python
class simulation:

class filters:

class plotting:
```

## tools3d.py:

Classes of functions in this module.

```python
class simulation:

class filters:

class plotting:
```

## figures:
* Streamwise velocity along the central line of flow(U_cl), time averaged 
![timeave_v_centralline](figures/timeave_v_centralline.png?raw=true "timeave_v_centralline")
* U_cl with some experimental results
![withexperimentaldata](figures/withexperimentaldata.png?raw=true "withexperimentaldata")
* Transverse profile at 6 positions in the wake, time averaged 
![transverse_timeave_allin1](figures/transverse_timeave_allin1.png?raw=true "transverse_timeave_allin1")

![transverse_timeave_all](figures/transverse_timeave_all.png?raw=true "transverse_timeave_all")
* Drag coefficient in pressure expression (Cp)
![drag_coe_Cp_timeave](figures/drag_coe_Cp_timeave.png?raw=true "drag_coe_Cp_timeave")


## License
This project is licensed by [MIT](https://choosealicense.com/licenses/mit/).
