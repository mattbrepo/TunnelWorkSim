# TunnelWorkSim
A simulation for the construction of a tunnel using [SimPy](https://simpy.readthedocs.io/en/latest/) with a [tkinter](https://docs.python.org/3/library/tkinter.html) gui.

**Language: Python**

**Start: 2023**

## Why
I wanted to try [SimPy](https://simpy.readthedocs.io/en/latest/) which is a Python module for [discrete-event simulation](https://en.wikipedia.org/wiki/Discrete-event_simulation). I decided to use it to model the construction of a tunnel.

## The simulation
The idea is to simulate the construction of a tunnel. The dimensions of the tunnel limit the number of workers that can work simultaneously (_Number of working slots_). Each worker can work for a number of sessions (_Maximum working sessions_) after which the worker must take a "long" rest. A working session lasts for a random time determined using an _Average working session time_ and after which the worker takes a "short" rest (_Average resting time_).

The simulation lasts for 10 day (240 hours) and the worked performed is measured in [man-hours](https://en.wikipedia.org/wiki/Man-hour).

## GUI
I also developed a simple GUI with [CustomTinker](https://github.com/TomSchimansky/CustomTkinter/wiki) to test different parameters:

![gui](/images/gui.jpg)
