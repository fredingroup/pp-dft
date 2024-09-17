# What is this?
- a Gui that simplifies the process of reading Multiwvn output files related to quantum chemical computations of electronic excitations in organic molecules

# How to run
- Check that the required modules are installed
- navigate to the `src` folder
- run `python index.py`
- input parameters in Gui
- pray
- look at your pretty graphs

# Requirements
- numpy
- pandas
- matplotlib.pyplots
- pyqt5

# To-Do:
- clean up plots
- add delete button to added states list
- add plotting function with interpolation between states (and interpolation selector)
- add state mixing capabilities
- include the multiwfn operation so I can just read .fchks

# To-Do - Larger Scope
- implement jablonski capabilities - with molecule selector

# Notes
- I'll just make my thing call multiwfn...


- multiwfn menu:
- - filename.fchk
- - 18
- - 5
- - filename.log
- - 2
- - 0
- - q


- in multiwfn_src_linux/multiwfn.f90 
- - line 284 print menu (choose 18)
- - line 508 call excittrans_main

- in multiwfn_src_linux/excittrans.f90
- - line 69 print menu (choose 5)
- - line 3600 calculate electric dipole moments

- in multiwfn_src_linux/fileIO.f90
- - line 400 read fchk
