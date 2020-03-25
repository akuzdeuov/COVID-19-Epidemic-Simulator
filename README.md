# COVID-19-Stochastic-Simulator
A modified version of Discrete Time Markov Chain based simulator proposed in this paper:

https://ieeexplore.ieee.org/document/7591271

The simulator capable of simulating SEQISR (susceptible, exposed, quarantined, infected, severe infected and recovered) model can be reduced to simpler models by setting some of the parameters (transition probabilities) to zero. 


**Prerequisites**
1. Ubuntu 16.04
2. Python 3
3. NumPy
4. Matplotlib

**How to install?**

Download and unzip files, or just simply clone files. 
Then type the following command on your terminal: 

 pip install -e /path/to/folder/setup.py 
 
 **How to run?**
 
 Open the terminal and insert the following command: covid19_simulator
 
 **Output**
 
 ![plot](https://raw.githubusercontent.com/akuzdeuov/COVID-19-Stochastic-Simulator/master/plot.png)
 
 **How to create .exe file from .py file?**
 
 https://www.youtube.com/watch?v=RM0K6Kq-Yho 

**Algorithm Pipeline**
![image](https://raw.githubusercontent.com/akuzdeuov/COVID-19-Stochastic-Simulator/master/covid_epidemic_statechart_hav2.png)
