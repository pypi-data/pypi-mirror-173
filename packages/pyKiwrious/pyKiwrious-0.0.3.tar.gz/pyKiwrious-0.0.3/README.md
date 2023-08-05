pyKiwrious
==========

[Overview](#overview)  
[Documentation](#documentations)  
[Tests and Demonstrations](#tests-and-demonstrations)  
[Installation](#installation)  
[Development](#development)  
[Future Plans](#future-plans)  
[Acknowledgement](#acknowledgement)  


Overview
--------
This repository contains the first implementation of the pyKiwrious library. 
The library supports Python development when working with [Kiwrious](https://kiwrious.com/) sensors. 
Using this library, you can connect with, read from, and manipulate Kiwrious streams through the `KiwriousService` object. 

- Project Homepage: https://github.com/uoa-compsci399-s2-2022/team36


Documentations
--------------
For detailed documentation of the functionalities, see the [PyPI_PublicationDetails.txt](https://github.com/uoa-compsci399-s2-2022/team36/blob/main/PyPI_PublicationDetails.txt) file.
For more details about the project and Kiwrious sensors, see the [report.pdf](coming soon) file.


Tests and Demonstrations
------------------------
Demonstrations on the usage of the library can be found in the [Demo](https://github.com/uoa-compsci399-s2-2022/team36/tree/main/Demos) directory.  
Tests can be found in the [testing](https://github.com/uoa-compsci399-s2-2022/team36/tree/main/Kiwrious/testing) directory (humidity, conductivity and heartbeat sensors), and the [Test Group](https://github.com/uoa-compsci399-s2-2022/team36/tree/main/Kiwrious/Test%20Group) directory (light, temperature and air quality sensors).  
Note: Demonstration programs and some tests are not publish to PyPi, but are all avaliable in github


Installation
------------
Start with using ``pip install pyKiwrious`` on your Python console.  
The library requires `pyserial` and `numpy`. This will be automatically imported by the setup.py file on installation.   
Alternatively, you can download the library from the PyPi page.


Development
-----------
The program is developed entirely with Python language (python>=3.0). It uses external libraries to connect with USB device (pyserial==3.5), and perform FFT to filter data (numpy==1.23.4). Aside from these essential tools, others were used to support developemnt.   
  
During early stages of development, we used the following tools:  
 - Bus hound software (version=6.0) to understand data structure. 
 - Visualisation tools to understand heart rate sensor (matplotlib==3.6.1).  

 For testing we used:
 - Testing tools (unittest==0.0) to develop test stubs.
 - Virtual serial port to simulate comports. 

To demonstrate the flexibility of our core library, demo programs used:
- Pygame
- Pyzero
- PushOver platform
- ONVIF-based CCTV camera 
- Rasberry Pi hardware and platform   
  
Project management was done through the following platforms:  
- Slack for client communications
- Github pull requests for version control  
- Wechat group communication
- Following Ganzt chart produced by ProjectLibre

Future Plans
------------
The current version can cause some delay when being used by end programs, this may cause major satisfaction when providing service for games and other programs that requires fast response. Future versions should develop techniques such as, thread pools, concurrency locks, and more to optimise resource allocation across the threads, hence lower latency.   
  
The program only provides basic functionality in reading data stream, future versions might benefit from implementing other functions such as, getting data average, controlling sample rate, getting data peak values and more that helps end program manipulate data. 


Acknowledgement
---------------
The project is developed by Team 36 from the UOA COMPSCI 399 course (2022, S2).  
Thank you for the support from our client and partner [Kiwrious](https://ahlab.org/project/kiwrious/) - Augmented Human Lab.
