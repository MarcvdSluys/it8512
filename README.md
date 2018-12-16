# ITech IT8512 Python Library

The [Itech IT8512](http://www.itech.sh/en/products.jsp?id=12&sortid=001008) is a programmable DC electronic load. 

It is a copy of the [BK precision 8500](http://www.bkprecision.com/products/dc-electronic-loads/8500-300-w-programmable-dc-electronic-load.html). It has a serial port for remote control and monitoring, and some windows software. Luckily the BK 8500 comes with a python library! The library is available with an MIT license from the link above. The BK software package comes with a more in depth demonstration and a decent PDF.

This repo contains a slightly modified version of the client to work with Linux systems. 

It also contains a script I wrote to do solar panel maximum power point tracking to determine current at maximum power point. Tracking algo is modified incremental-conductance (IC) to reduce the time to find maximum power point. An example of its output at very low light condition (<50 W/m2) and decreasing irridiation:

Set to remote control
Vset  voltsN ampsN voltsP deltaV sVoD deltaW watts
      12.435 0.001  0.000  0.000       0.000  0.000
09.32 09.309 0.004 12.435 -3.126 2.56 +0.035  0.035
06.76 06.749 0.006 09.309 -2.560 2.56 +0.004  0.039
04.20 04.189 0.008 06.749 -2.560 2.56 -0.006  0.033
06.76 06.749 0.006 04.189 +2.560 1.28 +0.005  0.038
08.04 08.030 0.005 06.749 +1.281 1.28 +0.000  0.038
09.32 09.311 0.004 08.030 +1.281 1.28 -0.004  0.034
08.04 08.030 0.005 09.311 -1.281 0.64 +0.003  0.037
07.40 07.389 0.005 08.030 -0.641 0.64 +0.002  0.039
06.76 06.750 0.006 07.389 -0.639 0.64 -0.001  0.038
07.40 07.389 0.005 06.750 +0.639 0.32 +0.000  0.038
07.08 07.069 0.005 07.389 -0.320 0.16 +0.000  0.038
06.92 06.929 0.005 07.069 -0.140 0.16 -0.001  0.037
07.08 07.069 0.005 06.929 +0.140 0.08 +0.001  0.038
07.16 07.150 0.005 07.069 +0.081 0.08 +0.000  0.038
07.08 07.077 0.005 07.150 -0.073 0.04 -0.001  0.037
07.12 07.110 0.005 07.077 +0.033 0.02 +0.000  0.037
07.14 07.128 0.005 07.110 +0.018 0.02 +0.000  0.037
07.16 07.148 0.005 07.128 +0.020 0.02 +0.000  0.037
07.18 07.168 0.005 07.148 +0.020 0.02 +0.000  0.037
07.20 07.188 0.005 07.168 +0.020 0.02 +0.000  0.037
07.18 07.188 0.005 07.188 +0.000 0.01 +0.000  0.037
07.17 07.164 0.005 07.188 -0.024 0.01 +0.000  0.037
MPPT found in 8.69 seconds

And another example around 100 W/m2 with increasing irridiation:
Set to remote control
Vset  voltsN ampsN voltsP deltaV sVoD deltaW watts
      25.134 0.001  0.000  0.000       0.000  0.000
18.85 18.838 0.007 25.134 -6.296 5.12 +0.137  0.137
13.73 13.721 0.012 18.838 -5.117 5.12 +0.027  0.164
08.61 08.599 0.016 13.721 -5.122 5.12 -0.024  0.140
13.73 13.721 0.012 08.599 +5.122 2.56 +0.024  0.164
16.29 16.281 0.010 13.721 +2.560 2.56 -0.006  0.158
13.73 13.720 0.012 16.281 -2.561 1.28 +0.006  0.164
12.45 12.442 0.013 13.720 -1.278 1.28 -0.002  0.162
13.73 13.720 0.012 12.442 +1.278 0.64 +0.002  0.164
14.37 14.363 0.011 13.720 +0.643 0.64 +0.000  0.164
15.01 15.001 0.011 14.363 +0.638 0.64 -0.001  0.163
14.37 14.363 0.011 15.001 -0.638 0.32 +0.001  0.164
14.05 14.041 0.012 14.363 -0.322 0.32 +0.000  0.164
14.37 14.363 0.011 14.041 +0.322 0.16 +0.000  0.164
14.53 14.523 0.011 14.363 +0.160 0.16 +0.000  0.164
14.69 14.682 0.011 14.523 +0.159 0.16 +0.000  0.164
14.53 14.539 0.011 14.682 -0.143 0.08 +0.000  0.164
14.45 14.454 0.011 14.539 -0.085 0.08 +0.001  0.165
14.37 14.372 0.011 14.454 -0.082 0.08 -0.001  0.164
14.45 14.443 0.011 14.372 +0.071 0.04 +0.001  0.165
14.49 14.477 0.011 14.443 +0.034 0.04 +0.000  0.165
14.53 14.515 0.011 14.477 +0.038 0.04 -0.001  0.164
14.49 14.484 0.011 14.515 -0.031 0.02 +0.001  0.165
14.47 14.484 0.011 14.484 +0.000 0.02 +0.000  0.165
14.49 14.484 0.011 14.484 +0.000 0.01 +0.000  0.165
MPPT found in 9.36 seconds
