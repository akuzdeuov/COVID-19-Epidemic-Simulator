# COVID-19-Epidemic-Simulator
A modified version of Discrete Time Markov Chain based simulator proposed in this paper:

https://ieeexplore.ieee.org/document/7591271

The simulator capable of simulating **SEQISR (susceptible, exposed, quarantined, infected, severe infected and recovered)** model can be reduced to simpler models by setting some of the parameters (transition probabilities) to zero. 


**Prerequisites**
1. Ubuntu 16.04
2. Python 3
3. NumPy
4. Matplotlib


**How to install?**

Download and unzip files, or just simply clone files. 
Then type the following command on your terminal: 

 *pip install -e /path/to/folder/setup.py* 
 
 **How to run?**
 
 Open the terminal and insert the following command: 
 
 *covid19_simulator*
 
 **Output**
 
 ![plot](https://raw.githubusercontent.com/akuzdeuov/COVID-19-Stochastic-Simulator/master/plot.png)
 
 **How to create .exe file from .py file?**
 1. Install Pyinstaller if you don't have it: *sudo pip3 install Pyinstaller*
 2. *pyinstaller --onefile covid19_simulator.py*
 3. The previous command generates two folders: **_build_** and **_dist_**. The generated **_covid19_simulator.exe_** is inside **_dist_** folder. To execute this file: *./covid19_simulator.exe*
 
 https://www.youtube.com/watch?v=RM0K6Kq-Yho 

**Algorithm Pipeline**
![image](https://raw.githubusercontent.com/akuzdeuov/COVID-19-Stochastic-Simulator/master/covid_epidemic_statechart.png)
