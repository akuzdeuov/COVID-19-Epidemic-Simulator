# COVID-19-Epidemic-Simulator
A modified version of Discrete Time Markov Chain based simulator proposed in this paper:

https://ieeexplore.ieee.org/document/7591271

The simulator capable of simulating **SEQISR (susceptible, exposed, quarantined, infected, severe infected and recovered)** model can be reduced to simpler models by setting some of the parameters (transition probabilities) to zero. 


**Prerequisites**
1. Ubuntu 16.04
2. Python 3
3. NumPy
4. Matplotlib
5. Qt Creator 4.11.1 (If we want to use GUI)


 **How to run without GUI?**
 
In this case all initial parameters need to be set manually. After setting parameters, open the terminal and insert the following command: 
 
 *python covid19_simulator_v2.py*
 
 **Output**
 
 ![plot](https://raw.githubusercontent.com/akuzdeuov/COVID-19-Stochastic-Simulator/master/plot.png)
 
 **How to run with GUI?**
 
GUI allows you set parameters without opening the files. If you have successfully installed Qt Creator then you should be able to open *covid19_simulator_qt* project.
 
 ![gui](https://raw.githubusercontent.com/akuzdeuov/COVID-19-Epidemic-Simulator/master/qt_gui.png)
 
 
![image](https://raw.githubusercontent.com/akuzdeuov/COVID-19-Epidemic-Simulator/master/covid_epidemic_statechart_v2.png)
