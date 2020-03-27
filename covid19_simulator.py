#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:24:35 2020

@author: askat
"""

import random
import numpy as np
import time 
import matplotlib.pyplot as plt 


class Node:
    def __init__(self):
        self.param_br = 0.0           # Daily birth rate
        self.param_dr = 0.0           # Daily mortality rate except infected people
        self.param_vr = 0.0           # Daily vaccination rate (Ratio of susceptible 
                                      # population getting vaccinated)
        self.param_vir = 0.9          # Ratio of the immunized after vaccination
        self.param_mir = 0.0          # Maternal immunization rate
        
        self.param_beta_exp = 0.1     # Susceptible to exposed transition constant
        self.param_qr  = 0.02         # Daily quarantine rate (Ratio of Exposed getting Quarantined)
        self.param_beta_inf = 0.0     # Susceptible to infected transition constant
        self.param_sir  = 0.01        # Daily severe infected rate (Ratio of Infected getting Severe Infected)
        
        self.param_eps_exp = 0.7      # Disease transmission rate of exposed compared to the infected
        self.param_eps_qua = 0.3      # Disease transmission rate of quarantined compared to the infected
        self.param_eps_sev = 0.3      # Disease transmission rate of severe infected compared to the infected
        
        self.param_hosp_capacity = 3000;  # Maximum amount patients that hospital can accommodate
        
        self.param_gamma_mor = 0.0    # Infected to Dead transition probability
        self.param_gamma_mor1 = 0.03; # Severe Infected (Hospitalized) to Dead transition probability
        self.param_gamma_mor2 = 0.1;  # Severe Infected (Not Hospitalized) to Dead transition probability
        self.param_gamma_im = 0.9     # Infected to Recovery Immunized transition probability
        
        self.param_dt = 1/24          # Sampling time in days (1/24 corresponds to one hour)
        self.param_sim_len = 365      # Length of simulation in days
        self.param_num_states = 0     # Number of states
        self.param_num_sim = int(self.param_sim_len / self.param_dt) + 1       # Number of simulation
        
        self.param_t_exp = 5          # Incubation period (The period from the start of 
                                      # incubation to the end of the incubation state)
        self.param_t_inf = 14          # Infection period (The period from the start of 
                                      # infection to the end of the infection state)
        self.param_t_vac = 3          # Vaccination immunization period (The time to 
                                      # vaccinatization immunization after being vaccinated)
        
        self.param_n_exp = round(self.param_t_exp / self.param_dt) 
        self.param_n_inf = round(self.param_t_inf / self.param_dt) 
        self.param_n_vac = round(self.param_t_vac / self.param_dt) 
        
        self.param_disp_interval = 100
        self.param_vis_on = 1                  # Visualize results after simulation
        
        np.random.seed(1)
        self.param_rand_seed = np.random.randint(low = 1, high = 100, size = 625)
        
        # Define the initial values for the states
        self.init_susceptible = 1000000
        self.init_exposed = 10
        self.init_quarantined = 0
        self.init_infected = 0
        self.init_severe_infected = 0
        self.init_vaccination_imm = 0
        self.init_maternally_imm = 0
        self.init_recovery_imm = 0
        
        # Define states
        self.states_x = [0, self.init_susceptible]
        self.states_dx = []
        self.states_name = ['Birth', 'Susceptible']
        self.states_type = ['Birth', 'Susceptible']
        
        # Define transitions
        self.source = ['Birth', 'Birth']
        self.dest = ['Susceptible', 'Maternally_Immunized' ]
        self.source_ind = []
        self.dest_ind = []
        

    def check_init(self):
        if self.param_beta_exp == 0 and self.param_beta_inf == 0:
            print('[ERROR] Both beta_exp and beta_inf cannot be zero.')
            return 0
        elif self.param_beta_exp != 0 and self.param_beta_inf != 0:
            print('[ERROR] Both beta_exp and beta_inf cannot be non-zero.')
            return 0
        else:
            print("[INFO] Initialization was done properly!")
            return 1
            
            
    def create_states(self):
        
        # create some temporal variables
        n_vac = self.param_n_vac
        n_vac_exp = n_vac + self.param_n_exp
        n_vac_2exp = n_vac_exp + self.param_n_exp
        n_vac_2exp_inf = n_vac_2exp + self.param_n_inf
        n_vac_2exp_2inf = n_vac_2exp_inf + self.param_n_inf + 1
        count = len(self.states_name) - 1
        
        # loop to create states
        while count < n_vac_2exp_2inf:
            # Vaccinated States
            if count <= n_vac:
                self.states_name.append('Vaccinated_{}'.format(count))
                self.states_type.append('Susceptible')
            # Exposed States (Includes both exposed and quarantined)
            elif count > n_vac and count <= n_vac_exp:
                self.states_name.append('Exposed_{}'.format(count - n_vac))
                self.states_type.append('Exposed')
                if count == n_vac + 1:
                    self.states_x.append(self.init_exposed)
                    count += 1
                    continue
            elif count > n_vac_exp and count <= n_vac_2exp:
                self.states_name.append('Quarantined_{}'.format(count - n_vac_exp))
                self.states_type.append('Exposed')
                if count == n_vac_exp + 1:
                    self.states_x.append(self.init_quarantined)
                    count += 1
                    continue
            # Infected States (Includes both infected and isolated)
            elif count > n_vac_2exp and count <= n_vac_2exp_inf:
                self.states_name.append('Infected_{}'.format(count - n_vac_2exp))
                self.states_type.append('Infected')
                if count == n_vac_2exp + 1:
                    self.states_x.append(self.init_infected)
                    count += 1
                    continue
            else:
                self.states_name.append('Severe_Infected_{}'.format(count - n_vac_2exp_inf))
                self.states_type.append('Infected')
                if count == n_vac_2exp + 1:
                    self.states_x.append(self.init_isolated)
                    count += 1
                    continue
                
            self.states_x.append(0)
                
            count += 1
            
        # Add the Immunized and dead states
        self.states_name.append('Vaccination_Immunized')
        self.states_type.append('Immunized')
        self.states_x.append(self.init_vaccination_imm)

        self.states_name.append('Maternally_Immunized')
        self.states_type.append('Immunized')
        self.states_x.append(self.init_maternally_imm)

        self.states_name.append('Recovery_Immunized')
        self.states_type.append('Immunized')
        self.states_x.append(self.init_recovery_imm)

        self.states_name.append('Dead')
        self.states_type.append('Dead')
        self.states_x.append(0)
        
        #print(self.states_name)
        
        # convert states into numpy arrays
        # for fast processing
        self.states_x = np.asarray(self.states_x, dtype=np.float32)
        self.states_dx = np.zeros(self.states_x.shape, dtype=np.float32)
        #self.states_name = np.asarray(self.states_name, dtype=str)
        #self.states_type = np.asarray(self.states_type, dtype=str)

        # initialize number of states
        self.param_num_states = len(self.states_x)
        
        print("[INFO] States were created...")
        
        
    def create_transitions(self):
        # create some temporal variables
        count = len(self.source) - 1
        n_st = self.param_num_states 
        n_vac = self.param_n_vac
        n_exp = self.param_n_exp
        n_inf = self.param_n_inf
        
        # Transition 3 - Any State except Birth to Dead (Natural Mortality)
        for ind in range(count, n_st - 1):
            self.source.append(self.states_name[ind])
            self.dest.append('Dead')
            
        # Transition 4 - Susceptible to Vaccinated[1]
        if self.param_vr != 0:
            self.source.append('Susceptible')
            self.dest.append('Vaccinated_1')
            
        # Transition 5 - Vaccinated[i] to Vaccinated[i+1] until i+1 == n_vac
        if self.param_n_vac != 0:
            for ind in range(n_vac - 1):
                self.source.append(self.states_name[2 + ind])
                self.dest.append(self.states_name[3 + ind])
                
        if self.param_vr != 0:
            # Transition 6 - Vaccinated[n_vac] to Vaccination_Immunized
            self.source.append('Vaccinated_{}'.format(n_vac))
            self.dest.append('Vaccination_Immunized')
            
            # Transition 7 - Vaccinated[n_vac] to Susceptible
            self.source.append('Vaccinated_{}'.format(n_vac))
            self.dest.append('Susceptible')
            
        # Transition 8 - Susceptible to Exposed[1]
        if self.param_n_exp != 0:
            self.source.append('Susceptible')
            self.dest.append('Exposed_1')
                
        # Transition 9 - Susceptible to Infected[1]
        self.source.append('Susceptible')
        self.dest.append('Infected_1')
            
        # Transition 10 - Exposed[i] to Exposed[i+1] until i+1 == n_exp
        for ind in range(n_exp - 1):
            self.source.append('Exposed_{}'.format(ind + 1))
            self.dest.append('Exposed_{}'.format(ind + 2))
            
        # Transition 11 - Exposed[n_inc] to Infected[1]
        if self.param_n_exp != 0:
            self.source.append('Exposed_{}'.format(n_exp))
            self.dest.append('Infected_1')
            
        # Transition 12 - Exposed[i] to Quarantined[i+1] until i+1 == n_exp
        for ind in range(n_exp - 1):
            self.source.append('Exposed_{}'.format(ind + 1))
            self.dest.append('Quarantined_{}'.format(ind + 2))
            
        # Transition 13 - Quarantined[i] to Quarantined[i+1] until i+1 == n_exp
        for ind in range(n_exp - 1):
            self.source.append('Quarantined_{}'.format(ind + 1))
            self.dest.append('Quarantined_{}'.format(ind + 2))
            
        # Transition 14 - Quarantined[n_exp] to Infected[1]
        if self.param_n_exp != 0:
            self.source.append('Quarantined_{}'.format(n_exp))
            self.dest.append('Infected_1')
        
        # Transition 15 - Infected[i] to Infected[i+1] until i+1 == n_inf
        for ind in range(n_inf - 1):
            self.source.append('Infected_{}'.format(ind + 1))
            self.dest.append('Infected_{}'.format(ind + 2))
            
        # Transition 16 - Severe_Infected[i] to Severe_Infected[i+1] until i+1 == n_inf
        for ind in range(n_inf - 1):
            self.source.append('Severe_Infected_{}'.format(ind + 1))
            self.dest.append('Severe_Infected_{}'.format(ind + 2))
            
        # Transition 17 - Infected[i] to Severe_Infected[i+1] until i+1 == n_inf
        for ind in range(n_inf - 1):
            self.source.append('Infected_{}'.format(ind + 1))
            self.dest.append('Severe_Infected_{}'.format(ind + 2))
            
        # Transition 18 - Infected[n_inf] to Recovery_Immunized
        self.source.append('Infected_{}'.format(n_inf))
        self.dest.append('Recovery_Immunized')
        
        # Transition 19 - Severe_Infected[n_inf] to Recovery Immunized
        self.source.append('Severe_Infected_{}'.format(n_inf))
        self.dest.append('Recovery_Immunized')
        
        # Transition 20 - Infected[n_inf] to Susceptible
        self.source.append('Infected_{}'.format(n_inf))
        self.dest.append('Susceptible')
        
        # Transition 21 - Severe_Infected[n_inf] to Susceptible
        self.source.append('Severe_Infected_{}'.format(n_inf))
        self.dest.append('Susceptible')
        
        # Transition 22 - Infected[n_inf] to Dead
        self.source.append('Infected_{}'.format(n_inf))
        self.dest.append('Dead')
        
        # Transition 23 - Severe_Infected[n_inf] to Dead
        self.source.append('Severe_Infected_{}'.format(n_inf))
        self.dest.append('Dead')
        
        for ind in range(len(self.source)):
            self.source_ind.append(self.states_name.index(self.source[ind]))
            self.dest_ind.append(self.states_name.index(self.dest[ind]))
        
        print("[INFO] State transitions were created...")


    def indexes(self):
        # define vectors of indices
        self.ind_vac = np.zeros((len(self.states_x)), dtype=np.float32)
        self.ind_inf = np.zeros((len(self.states_x)), dtype=np.float32)
        self.ind_exp = np.zeros((len(self.states_x)), dtype=np.float32)
        self.ind_sin = np.zeros((len(self.states_x)), dtype=np.float32)
        self.ind_qua = np.zeros((len(self.states_x)), dtype=np.float32)
        self.ind_imm = np.zeros((len(self.states_x)), dtype=np.float32)
        self.ind_sus = np.zeros((len(self.states_x)), dtype=np.float32)
        
        # intialize vectors of indices
        for ind in range(len(self.states_name)):
            if self.states_name[ind] == 'Vaccinated_{}'.format(self.param_n_vac):
                self.ind_vac[ind] = 1
            elif 'Infected_' in self.states_name[ind] and not 'Severe_Infected_' in self.states_name[ind]:
                self.ind_inf[ind] = 1
            elif 'Exposed_' in self.states_name[ind]:
                self.ind_exp[ind] = 1
            elif 'Severe_Infected_' in self.states_name[ind]:
                self.ind_sin[ind] = 1
                #print(self.states_name[ind])
            elif 'Quarantined_' in self.states_name[ind]:
                self.ind_qua[ind] = 1
            elif 'Immunized' in self.states_type[ind]:
                self.ind_imm[ind] = 1
            elif 'Susceptible' in self.states_type[ind]:
                self.ind_sus[ind] = 1
        
        # define other indices
        self.ind_exp1 = self.states_name.index('Exposed_1')
        self.ind_expn = self.states_name.index('Exposed_{}'.format(self.param_n_exp))
        
        self.ind_qua1 = self.states_name.index('Quarantined_1')
        self.ind_quan = self.states_name.index('Quarantined_{}'.format(self.param_n_exp))
        
        self.ind_sin1 = self.states_name.index('Severe_Infected_1')
        self.ind_sinn = self.states_name.index('Severe_Infected_{}'.format(self.param_n_inf))
        
        self.ind_inf1 = self.states_name.index('Infected_1')
        self.ind_infn = self.states_name.index('Infected_{}'.format(self.param_n_inf))
        
    
        
    def dx_generator(self, size, val):
        dx = 0
      
        for ind in range(size):
            rand_num = random.uniform(0, 1)
            if rand_num < val:
                dx += 1
    
        return dx
    
    
    def stoch_solver(self):
        # define a list to store transitions
        expval = []
        state_1 = self.states_x[1]
                                
        # Total population is the sum of all states except birth and death
        total_pop = self.states_x[1:-1].sum()
        
        # Transition 1 - Birth to Susceptible
        expval.append(total_pop * self.param_br * (1 - self.param_mir) * self.param_dt)
        
        # Transition 2 - Birth to Maternally Immunized
        expval.append(total_pop * self.param_br * self.param_mir * self.param_dt)
        
        # Transition 3 - Any State except Birth to Dead (Natural Mortality)
        expval += (self.states_x[1:self.param_num_states - 1] * self.param_dr * self.param_dt).tolist()
   
        # Transition 4 - Susceptible to Vaccinated[1]
        if self.param_vr != 0:
            expval.append(state_1 * self.param_vr * self.param_dt)
            
        # Transition 5 - Vaccinated[i] to Vaccinated[i+1] until i+1 == n_vac
        if self.param_n_vac != 0:
            expval += (self.states_x[2:self.param_n_vac + 1] * \
                   (1 - self.param_dr * self.param_dt)).tolist()

        # Transition 6 - Vaccinated[n_vac] to Vaccination_Immunized
        # Transition 7 - Vaccinated[n_vac] to Susceptible
        if self.param_vr != 0:
            state_vac = self.states_x.dot(self.ind_vac).sum()
            expval.append(state_vac * self.param_vir)
            expval.append(state_vac * (1 - self.param_dr * self.param_dt - self.param_vir))
            
        # Transition 8 - Susceptible to Exposed[1]
        temp1 = self.states_x.dot(self.ind_inf).sum() + self.param_eps_exp * \
                self.states_x.dot(self.ind_exp).sum() + self.param_eps_sev * \
                self.states_x.dot(self.ind_sin).sum() + self.param_eps_qua * self.states_x.dot(self.ind_qua).sum()
            
        if self.param_n_exp != 0:
            expval.append(state_1 * temp1 * self.param_beta_exp * self.param_dt / total_pop)
            
        # Transition 9 - Susceptible to Infected[1] 
        expval.append(state_1 * temp1 * self.param_beta_inf * self.param_dt / total_pop)
        
        # Transition 10 - Exposed[i] to Exposed[i+1] until i+1 == n_exp
        expval += (self.states_x[self.ind_exp1:self.ind_exp1 + self.param_n_exp - 1] * \
                   (1 - self.param_dr * self.param_dt - self.param_qr * self.param_dt)).tolist()

        # Transition 11 - Exposed[n_exp] to Infected[1]
        if self.param_n_exp != 0:
            expval.append(self.states_x[self.ind_expn] * (1 - self.param_dr * self.param_dt))
            
        # Transition 12 - Exposed[i] to Quarantined[i+1] until i+1 == n_exp
        expval += (self.states_x[self.ind_exp1:self.ind_exp1 + self.param_n_exp - 1] * \
                  (self.param_qr * self.param_dt)).tolist()

        # Transition 13 - Quarantined[i] to Quarantined[i+1] until i+1 == n_exp
        expval += (self.states_x[self.ind_qua1:self.ind_qua1 + self.param_n_exp - 1] * \
                   (1 - self.param_dr * self.param_dt)).tolist()

        # Transition 14 - Quarantined[n_exp] to Infected[1]
        if self.param_n_exp != 0:
            expval.append(self.states_x[self.ind_quan] * (1 - self.param_dr * self.param_dt))
            
        # Transition 15 - Infected[i] to Infected[i+1] until i+1 == n_inf
        expval += (self.states_x[self.ind_inf1:self.ind_inf1 + self.param_n_inf - 1] * \
                   (1 - self.param_dr * self.param_dt - self.param_sir * self.param_dt)).tolist()
     
        # Transition 16 - Severe_Infected[i] to Severe_Infected[i+1] until i+1 == n_inf
        expval += (self.states_x[self.ind_sin1:self.ind_sin1 + self.param_n_inf - 1] * \
                   (1 - self.param_dr * self.param_dt)).tolist()
         
        # Transition 17 - Infected[i] to Severe_Infected[i+1] until i+1 == n_inf
        expval += (self.states_x[self.ind_inf1:self.ind_inf1 + self.param_n_inf - 1] * \
                   (self.param_sir * self.param_dt)).tolist()

        # Transition 18 - Infected[n_inf] to Recovery_Immunized
        expval.append(self.states_x[self.ind_infn] * self.param_gamma_im)
        
        # Transition 19 - Severe_Infected[n_inf] to Recovery Immunized
        expval.append(self.states_x[self.ind_sinn] * self.param_gamma_im)
        
        # Transition 20 - Infected[n_inf] to Susceptible
        expval.append(self.states_x[self.ind_infn] * \
                          (1 - self.param_gamma_mor - self.param_gamma_im))
            
        # Transition 21 - Severe_Infected[n_inf] to Susceptible
        states_sin = self.states_x.dot(self.ind_sin).sum()
        
        if states_sin < self.param_hosp_capacity:
            expval.append(self.states_x[self.ind_sinn] * \
                          (1 - self.param_gamma_mor1 - self.param_gamma_im))
        else:
            expval.append(self.states_x[self.ind_sinn] * \
                          (1 - self.param_gamma_mor2 - self.param_gamma_im))
            
        # Transition 22 - Infected[n_inf] to Dead
        expval.append(self.states_x[self.ind_infn] * self.param_gamma_mor)
        
        # Transition 23 - Severe_Infected[n_inf] to Dead
        if states_sin < self.param_hosp_capacity:
            expval.append(self.states_x[self.ind_sinn] *self.param_gamma_mor1) 
        else:
            expval.append(self.states_x[self.ind_sinn] *self.param_gamma_mor2)
        
        # Randomly generate the transition value based on the expected value
        for eval, sind, dind in zip(expval, self.source_ind, self.dest_ind):
            if eval < 10:
                temp1 = int(np.ceil(eval * 10 + np.finfo(np.float32).eps))
                temp2 = eval/temp1
                dx = self.dx_generator(temp1, temp2)
            else:
                dx = round(eval)
     
            # Apply the changes for the transitions to the 
            # corresponding source and destination states     
            temp = self.states_x[sind] - dx
            
            if sind == 1:
                self.states_x[sind] = temp
                self.states_x[dind] += dx
            elif temp <= 0:
                self.states_x[dind] += self.states_x[sind]
                self.states_x[sind] = 0
            else:
                self.states_x[sind] = temp 
                self.states_x[dind] += dx
        

def main():
    # initialize a new node            
    node = Node()
    
    # check correctenes of the initialization 
    if node.check_init():
        # create states based on the
        # initialization parameters
        node.create_states()
        node.indexes()
        
        # create transitions based on 
        # the created states
        node.create_transitions()
    
        # create a container to store states
        states_arr = np.zeros((node.param_num_sim, len(node.states_name)), dtype=np.float32)
    
        start = time.time()
        # start simulation
        for ind in range(node.param_num_sim):
            states_arr[ind, :] = node.states_x
            node.stoch_solver()
            
            if ind % node.param_disp_interval == 0:
                end = time.time()
                print("Sim.time: {:.4f} sec, Iteration: {}/{}".format(end - start, ind + 1, node.param_num_sim))
        
        # if visualization is enabled
        # then plot states
        if node.param_vis_on:
            # extract all states from states array    
            time_arr = np.linspace(0, node.param_num_sim, node.param_num_sim) * node.param_dt
            state_sus = states_arr.dot(node.ind_sus)
            state_exp = states_arr.dot(node.ind_exp)
            state_inf = states_arr.dot(node.ind_inf)
            state_sin = states_arr.dot(node.ind_sin)
            state_qua = states_arr.dot(node.ind_qua)
            state_imm = states_arr.dot(node.ind_imm)
            state_dea = states_arr[:, -1]
        
            fig, ax = plt.subplots(figsize=(8,4))
            ax.plot(time_arr, state_sus, linewidth=1, color='dodgerblue', label = 'Susceptible')
            ax.plot(time_arr, state_exp, linewidth=1, color='lime', linestyle = ':',  label = 'Exposed')
            ax.plot(time_arr, state_qua, linewidth=1, color='fuchsia', linestyle = '-.', label = 'Quarantined')
            ax.plot(time_arr, state_inf, linewidth=1, color='navy', linestyle = '--', label = 'Infected')
            ax.plot(time_arr, state_sin, linewidth=1, color='r', linestyle = '--', label = 'Severe Infected')
            ax.plot(time_arr, state_imm, linewidth=1, color='cyan', label = 'Immunized')
            ax.plot(time_arr, state_dea, linewidth=1, color='k', label = 'Dead')
            plt.ylim(0,node.init_susceptible)
            plt.xlim(0,node.param_sim_len)
            ax.grid(linestyle=':', linewidth=1)
            plt.ylabel("Number of individuals", fontsize=18)
            plt.legend(loc="upper left", ncol=1)
            
            ax2 = plt.axes([0.125, -0.2, 0.778, 0.2])
            ax2.plot(time_arr, state_sin, linewidth=1, color='r', linestyle = '--', label = 'Severe Infected')
            ax2.plot(time_arr, np.ones(node.param_num_sim) * node.param_hosp_capacity, linewidth=1, color='lime', label = 'Hospital Capacity')
            ax2.plot(time_arr, state_dea, linewidth=1, color='k', label = 'Dead')
            plt.xlabel("Time (days)", fontsize=18)
            plt.legend(loc="upper left", ncol=1)
            ax2.grid(linestyle=':', linewidth=1)
            plt.show()
        
    
if __name__ == "__main__":
    main()
