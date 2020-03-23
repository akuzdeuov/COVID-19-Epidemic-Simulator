import numpy as np
import time 
import matplotlib.pyplot as plt 


class Node:
    def __init__(self):
        self.param_br = 0.02 / 365    # Daily birth rate
        self.param_dr = 0.01 / 365    # Daily mortality rate except infected people
        self.param_vr = 0.02          # Daily vaccination rate (Ratio of susceptible 
                                       # population getting vaccinated)
        self.param_vir = 0.9          # Ratio of the immunized after vaccination
        self.param_mir = 0.0          # Maternal immunization rate
        self.param_beta_exp = 0.5     # Susceptible to exposed transition constant
        self.param_qr  = 0.1          # Daily quarantine rate (Ratio of Exposed getting Quarantined)
        self.param_beta_inf = 0.0     # Susceptible to infected transition constant
        self.param_ir  = 0.1          # Daily isolation rate (Ratio of Infected getting Isolated)
        
        self.param_eps_exp = 0.7      # Disease transmission rate of exposed compared to the infected
        self.param_eps_qua = 0.3      # Disease transmission rate of quarantined compared to the infected
        self.param_eps_iso = 0.3      # Disease transmission rate of isolated compared to the
        
        self.param_gamma_mor = 0.4    # Infected to Dead transition probability
        self.param_gamma_im = 0.0     # Infected to Recovery Immunized transition probability
        
        self.param_dt = 1/24          # Sampling time in days (1/24 corresponds to one hour)
        self.param_sim_len = 100      # Length of simulation in days
        self.param_num_states = 0     # Number of states
        self.param_num_sim = int(self.param_sim_len / self.param_dt) + 1       # Number of simulation
        
        self.param_t_exp = 3          # Incubation period (The period from the start of 
                                      # incubation to the end of the incubation state)
        self.param_t_inf = 5          # Infection period (The period from the start of 
                                      # infection to the end of the infection state)
        self.param_t_vac = 3          # Vaccination immunization period (The time to 
                                      # vaccinatization immunization after being vaccinated)
        self.param_n_exp = int(self.param_t_exp / self.param_dt)
        self.param_n_inf = int(self.param_t_inf / self.param_dt)
        self.param_n_vac = int(self.param_t_vac / self.param_dt)
        
        self.param_save_res = 1
        self.param_disp_progress = 1
        self.param_disp_interval = 100
        self.param_vis_on = 1                  # Visualize results after simulation
        
        np.random.seed(1)
        self.param_rand_seed = np.random.randint(low = 1, high = 100, size = 625)
        
        # Define the initial values for the states
        self.init_susceptible = 9990
        self.init_exposed = 10
        self.init_quarantined = 0
        self.init_infected = 0
        self.init_isolated = 0
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
        
        # Define transitions in stochastic solver
        self.expval = []
        
        
    def check_init(self):
        if self.param_beta_exp == 0 and self.param_beta_inf == 0:
            print('[ERROR] Both beta_exp and beta_inf cannot be zero.')
        elif self.param_beta_exp != 0 and self.param_beta_inf != 0:
            print('[ERROR] Both beta_exp and beta_inf cannot be non-zero.')
        else:
            print("[INFO] Initialization was done properly!")
            
            
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
                self.states_name.append('Isolated_{}'.format(count - n_vac_2exp_inf))
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
            
        # Transition 14 - Quarantined[n_exp] to Isolated[1]
        if self.param_n_exp != 0:
            self.source.append('Quarantined_{}'.format(n_exp))
            self.dest.append('Isolated_1')
        
        # Transition 15 - Infected[i] to Infected[i+1] until i+1 == n_inf
        for ind in range(n_inf - 1):
            self.source.append('Infected_{}'.format(ind + 1))
            self.dest.append('Infected_{}'.format(ind + 2))
            
        # Transition 16 - Isolated[i] to Isolated[i+1] until i+1 == n_inf
        for ind in range(n_inf - 1):
            self.source.append('Isolated_{}'.format(ind + 1))
            self.dest.append('Isolated_{}'.format(ind + 2))
            
        # Transition 17 - Infected[i] to Isolated[i+1] until i+1 == n_inf
        for ind in range(n_inf - 1):
            self.source.append('Infected_{}'.format(ind + 1))
            self.dest.append('Isolated_{}'.format(ind + 2))
            
        # Transition 18 - Infected[n_inf] to Recovery_Immunized
        self.source.append('Infected_{}'.format(n_inf))
        self.dest.append('Recovery_Immunized')
        
        # Transition 19 - Isolated[n_inf] to Recovery Immunized
        self.source.append('Isolated_{}'.format(n_inf))
        self.dest.append('Recovery_Immunized')
        
        # Transition 20 - Infected[n_inf] to Susceptible
        self.source.append('Infected_{}'.format(n_inf))
        self.dest.append('Susceptible')
        
        # Transition 21 - Isolated[n_inf] to Susceptible
        self.source.append('Isolated_{}'.format(n_inf))
        self.dest.append('Susceptible')
        
        # Transition 22 - Infected[n_inf] to Dead
        self.source.append('Infected_{}'.format(n_inf))
        self.dest.append('Dead')
        
        # Transition 23 - Isolated[n_inf] to Dead
        self.source.append('Isolated_{}'.format(n_inf))
        self.dest.append('Dead')
        
        for ind in range(len(self.source)):
            self.source_ind.append(self.states_name.index(self.source[ind]))
            self.dest_ind.append(self.states_name.index(self.dest[ind]))

        print("[INFO] State transitions were created...")

        
    def stoch_solver(self):
        # define vectors of indices
        ind_vac = np.zeros((len(self.states_x)), dtype=np.float32)
        ind_inf = np.zeros((len(self.states_x)), dtype=np.float32)
        ind_exp = np.zeros((len(self.states_x)), dtype=np.float32)
        ind_iso = np.zeros((len(self.states_x)), dtype=np.float32)
        ind_qua = np.zeros((len(self.states_x)), dtype=np.float32)
        
        # intialize vectors of indices
        for ind in range(len(self.states_name)):
            if self.states_name[ind] == 'Vaccinated_{}'.format(self.param_n_vac):
                ind_vac[ind] = 1
            elif 'Infected_' in self.states_name[ind]:
                ind_inf[ind] = 1
            elif 'Exposed_' in self.states_name[ind]:
                ind_exp[ind] = 1
            elif 'Isolated_' in self.states_name[ind]:
                ind_iso[ind] = 1
            elif 'Quarantined_' in self.states_name[ind]:
                ind_qua[ind] = 1
                
        # define other indices
        ind_exp1 = self.states_name.index('Exposed_1')
        ind_expn = self.states_name.index('Exposed_{}'.format(self.param_n_exp))
        
        ind_qua1 = self.states_name.index('Quarantined_1')
        ind_quan = self.states_name.index('Quarantined_{}'.format(self.param_n_exp))
        
        ind_iso1 = self.states_name.index('Isolated_1')
        ind_ison = self.states_name.index('Isolated_{}'.format(self.param_n_inf))
        
        ind_inf1 = self.states_name.index('Infected_1')
        ind_infn = self.states_name.index('Infected_{}'.format(self.param_n_inf))
                        
        # Total population is the sum of all states except birth and death
        total_pop = np.sum(self.states_x[1:-1])
        
        # Transition 1 - Birth to Susceptible
        self.expval.append(total_pop * self.param_br * (1 - self.param_mir) * self.param_dt)
        
        # Transition 2 - Birth to Maternally Immunized
        self.expval.append(total_pop * self.param_br * self.param_mir * self.param_dt)
        
        # Transition 3 - Any State except Birth to Dead (Natural Mortality)
        for ind in range(1, self.param_num_states - 1):
            self.expval.append(self.states_x[ind] * self.param_dr * self.param_dt)
            
        # Transition 4 - Susceptible to Vaccinated[1]
        if self.param_vr != 0:
            self.expval.append(self.states_x[1] * self.param_vr * self.param_dt)
            
        # Transition 5 - Vaccinated[i] to Vaccinated[i+1] until i+1 == n_vac
        if self.param_n_vac != 0:
            for ind in range(self.param_n_vac - 1):
                self.expval.append(self.states_x[2 + ind] * (1 - self.param_dr * self.param_dt))
                
        # Transition 6 - Vaccinated[n_vac] to Vaccination_Immunized
        # Transition 7 - Vaccinated[n_vac] to Susceptible
        if self.param_vr != 0:
            self.expval.append(np.sum(np.multiply(self.states_x, ind_vac)) * self.param_vir)
            self.expval.append(np.sum(np.multiply(self.states_x, ind_vac)) * 
                               (1 - self.param_dr * self.param_dt - self.param_vir))
            
        # Transition 8 - Susceptible to Exposed[1]
        if self.param_n_exp != 0:
            temp1 = np.sum(np.multiply(self.states_x, ind_inf)) + self.param_eps_exp * \
            np.sum(np.multiply(self.states_x, ind_exp)) + self.param_eps_iso * \
                np.sum(np.multiply(self.states_x, ind_iso)) + \
            self.param_eps_qua * np.sum(np.multiply(self.states_x, ind_qua))
            
            self.expval.append(self.states_x[1] * temp1 * self.param_beta_exp * self.param_dt / total_pop)
            
        # Transition 9 - Susceptible to Infected[1] 
        temp1 = np.sum(np.multiply(self.states_x, ind_inf)) + self.param_eps_exp * \
            np.sum(np.multiply(self.states_x, ind_exp)) + self.param_eps_iso * \
                np.sum(np.multiply(self.states_x, ind_iso)) + \
            self.param_eps_qua * np.sum(np.multiply(self.states_x, ind_qua))
        self.expval.append(self.states_x[1] * temp1 * self.param_beta_inf * self.param_dt / total_pop)
        
        # Transition 10 - Exposed[i] to Exposed[i+1] until i+1 == n_exp
        for ind in range(self.param_n_exp - 1):
            self.expval.append(self.states_x[ind_exp1 + ind] * \
                (1 - self.param_dr * self.param_dt - self.param_qr * self.param_dt))
       
        # Transition 11 - Exposed[n_exp] to Infected[1]
        if self.param_n_exp != 0:
            self.expval.append(self.states_x[ind_expn] * (1 - self.param_dr * self.param_dt))
            
        # Transition 12 - Exposed[i] to Quarantined[i+1] until i+1 == n_exp
        for ind in range(self.param_n_exp - 1):
            self.expval.append(self.states_x[ind_exp1 + ind] * (self.param_qr * self.param_dt))
            
        # Transition 13 - Quarantined[i] to Quarantined[i+1] until i+1 == n_exp
        for ind in range(self.param_n_exp - 1):
            self.expval.append(self.states_x[ind_qua1 + ind] * (1 - self.param_dr * self.param_dt))
            
        # Transition 14 - Quarantined[n_exp] to Isolated[1]
        if self.param_n_exp != 0:
            self.expval.append(self.states_x[ind_quan] * (1 - self.param_dr * self.param_dt))
            
        # Transition 15 - Infected[i] to Infected[i+1] until i+1 == n_inf
        for ind in range(self.param_n_inf - 1):
            self.expval.append(self.states_x[ind_inf1 + ind] * \
                               (1 - self.param_dr * self.param_dt - self.param_ir * self.param_dt))
        
        # Transition 16 - Isolated[i] to Isolated[i+1] until i+1 == n_inf
        for ind in range(self.param_n_inf - 1):
            self.expval.append(self.states_x[ind_iso1 + ind] * \
                               (1 - self.param_dr * self.param_dt))
                
        # Transition 17 - Infected[i] to Isolated[i+1] until i+1 == n_inf
        for ind in range(self.param_n_inf - 1):
            self.expval.append(self.states_x[ind_inf1 + ind] * \
                               (self.param_ir * self.param_dt))
        
        # Transition 18 - Infected[n_inf] to Recovery_Immunized
        self.expval.append(self.states_x[ind_infn] * self.param_gamma_im)
        
        # Transition 19 - Isolated[n_inf] to Recovery Immunized
        self.expval.append(self.states_x[ind_ison] * self.param_gamma_im)
        
        # Transition 20 - Infected[n_inf] to Susceptible
        self.expval.append(self.states_x[ind_infn] * \
                          (1 - self.param_gamma_mor - self.param_gamma_im))
            
        # Transition 21 - Isolated[n_inf] to Susceptible
        self.expval.append(self.states_x[ind_ison] * \
                          (1 - self.param_gamma_mor - self.param_gamma_im))
            
        # Transition 22 - Infected[n_inf] to Dead
        self.expval.append(self.states_x[ind_infn] * self.param_gamma_mor)
        
        # Transition 23 - Isolated[n_inf] to Dead
        self.expval.append(self.states_x[ind_ison] * self.param_gamma_mor)
        
        # Randomly generate the transition value based on the expected value
        np_expval = np.asarray(self.expval, dtype=np.float32)
        dx = np.zeros(len(self.expval), dtype=np.float32)
        for ind in range(len(self.expval)):
            temp1 = np.ceil(np_expval[ind] * 10 + np.finfo(np.float32).eps)
            dx[ind] = np.sum((np.random.uniform(low=0.0, high=1.0, size=int(temp1)) < 
                             (np_expval[ind] / temp1)).astype(int))
            #if dx[ind] > 0:
                #print(ind, dx[ind])
        
        # Apply the changes for the transitions to the 
        # corresponding source and destination states
        for ind in range(len(self.expval)):
            sind = self.source_ind[ind]
            dind = self.dest_ind[ind]
            
            temp = self.states_x[sind] - dx[ind]
            
            if sind == 1:
                self.states_x[sind] = temp
                self.states_x[dind] = self.states_x[dind] + dx[ind]
            elif temp <= 0:
                self.states_x[dind] = self.states_x[dind] + self.states_x[sind]
                self.states_x[sind] = 0
            else:
                self.states_x[sind] = temp 
                self.states_x[dind] = self.states_x[dind] + dx[ind]
        
        self.states_dx = dx
        #for ind in range(len(self.expval)):
        #    if self.expval[ind] > 0:
        #        print(self.expval[ind], ind)
        
        self.expval = []
        

def main():
    # initialize a new node            
    node = Node()
    
    # check correctenes of the initialization 
    node.check_init()
    
    # create states based on the
    # initialization parameters
    node.create_states()
    
    # create transitions based on 
    # the created states
    node.create_transitions()
    
    # create a containers to store states
    states_arr = np.zeros((node.param_num_sim, len(node.states_name)), dtype=np.float32)
    
    start = time.time()
    for ind in range(node.param_num_sim):
        states_arr[ind, :] = node.states_x
        node.stoch_solver()
        
        if ind % node.param_disp_interval == 0:
            print("Iteration: {}/{}".format(ind + 1, node.param_num_sim))
        
    end = time.time()
    print("Simulation took {} sec".format(end - start))
    
    if node.param_vis_on:
        # define vectors of indices
        ind_vac = np.zeros((len(node.states_x)), dtype=np.float32)
        ind_inf = np.zeros((len(node.states_x)), dtype=np.float32)
        ind_exp = np.zeros((len(node.states_x)), dtype=np.float32)
        ind_iso = np.zeros((len(node.states_x)), dtype=np.float32)
        ind_qua = np.zeros((len(node.states_x)), dtype=np.float32)
        ind_imm = np.zeros((len(node.states_x)), dtype=np.float32)
        ind_sus = np.zeros((len(node.states_x)), dtype=np.float32)
        
        # intialize vectors of indices
        for ind in range(len(node.states_name)):
            if node.states_name[ind] == 'Vaccinated_{}'.format(node.param_n_vac):
                ind_vac[ind] = 1
            elif 'Infected_' in node.states_name[ind]:
                ind_inf[ind] = 1
            elif 'Exposed_' in node.states_name[ind]:
                ind_exp[ind] = 1
            elif 'Isolated_' in node.states_name[ind]:
                ind_iso[ind] = 1
            elif 'Quarantined_' in node.states_name[ind]:
                ind_qua[ind] = 1
            elif 'Immunized' in node.states_type[ind]:
                ind_imm[ind] = 1
            elif 'Susceptible' in node.states_type[ind]:
                ind_sus[ind] = 1
                
        time_arr = np.linspace(0, node.param_num_sim, node.param_num_sim) * node.param_dt
        state_sus = states_arr.dot(ind_sus)
        state_exp = states_arr.dot(ind_exp)
        state_inf = states_arr.dot(ind_inf)
        state_iso = states_arr.dot(ind_iso)
        state_qua = states_arr.dot(ind_qua)
        state_imm = states_arr.dot(ind_imm)
        state_dea = states_arr[:, -1]
        
        plt.plot(time_arr, state_sus, label = 'Susceptible')
        plt.plot(time_arr, state_exp, label = 'Exposed')
        plt.plot(time_arr, state_qua, label = 'Quarantined')
        plt.plot(time_arr, state_inf, label = 'Infected')
        plt.plot(time_arr, state_iso, label = 'Isolated')
        plt.plot(time_arr, state_imm, label = 'Immunized')
        plt.plot(time_arr, state_dea, label = 'Dead')
        plt.legend(loc="upper right")
        plt.show()
        
    
if __name__ == "__main__":
    main()
