Tatlin For Lasers... Xburn GUI
======

Tatlin is a Gcode and STL viewer heavily inspired by Mac-only software
Pleasant3D. Besides viewing, it also supports rotating and scaling of STL
files. It is currently in early stages of development, but should already
be quite usable.


This hacked up version supports creating burning paths for low power lasers attached to GRBL devices.
![Preview Image](testing.jpg?raw=true "Preview Image")


Dependencies
------------

Tatlin requires the following packages:

- Python 2.6+
- wxPython 2.8+
- PyOpenGL
- NumPy

Usage
-----

To launch Tatlin from the command line:

    $ python tatlin.py

You can also provide a filename to load:

    $ python tatlin.py foobar.jpg

Mouse navigation

* Left mouse button to rotate
* Mouse wheel to zoom
* Middle mouse button to offset the platform
* Right mouse button to pan

Build platform size can be customized by creating a file called `.tatlin` in
your home directory with the following contents:

    [machine]
    platform_w = 300
    platform_d = 300

Thanks
-------

* Lenbok for config file options
* Bartosz Zaborowski for the two digit Gcode patch
