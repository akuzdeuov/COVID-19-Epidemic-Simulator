import numpy as np 
import matlab.engine
import matplotlib.pyplot as plt 


class Node:
    def __init__(self):
        self.param_br = 0.02 / 365;    # Daily birth rate
        self.param_dr = 0.01 / 365;    # Daily mortality rate except infected people
        self.param_vr = 0.02;          # Daily vaccination rate (Ratio of susceptible 
                                       # population getting vaccinated)
        self.param_vir = 0.9;          # Ratio of the immunized after vaccination
        self.param_mir = 0.0;          # Maternal immunization rate
        self.param_beta_exp = 0.5;     # Susceptible to exposed transition constant
        self.param_qr  = 0.1;          # Daily quarantine rate (Ratio of Exposed getting Quarantined)
        self.param_beta_inf = 0.0;     # Susceptible to infected transition constant
        self.param_ir  = 0.1;          # Daily isolation rate (Ratio of Infected getting Isolated)
        
        self.param_eps_exp = 0.7;      # Disease transmission rate of exposed compared to the infected
        self.param_eps_qua = 0.3;      # Disease transmission rate of quarantined compared to the infected
        self.param_eps_iso = 0.3;      # Disease transmission rate of isolated compared to the
        
        self.param_gamma_mor = 0.4;    # Infected to Dead transition probability
        self.param_gamma_im = 0.0;     # Infected to Recovery Immunized transition probability
        
        self.param_dt = 1/24;          # Sampling time in days (1/24 corresponds to one hour)
        self.param_sim_len = 100;      # Length of simulation in days
        
        self.param_t_exp = 3;          # Incubation period (The period from the start of 
                                       # incubation to the end of the incubation state)
        self.param_t_inf = 5;          # Infection period (The period from the start of 
                                       # infection to the end of the infection state)
        self.param_t_vac = 3;          # Vaccination immunization period (The time to 
                                       # vaccinatization immunization after being vaccinated)
        self.param_n_exp = self.param_t_exp / self.param_dt
        self.param_n_inf = self.param_t_inf / self.param_dt
        self.param_n_vac = self.param_t_vac / self.param_dt
        
        self.param_save_res = 1;
        self.param_disp_progress = 1;
        self.param_disp_interval = 100;
        self.param_vis_on = 1;                  # Visualize results after simulation
        
        np.random.seed(1)
        self.param_rand_seed = np.random.randint(low = 1, high = 100, size = 625)
        
        # Define the initial values for the states
        self.init_susceptible = 9990;
        self.init_exposed = 10;
        self.init_quarantined = 0;
        self.init_infected = 0;
        self.init_isolated = 0;
        self.init_vaccination_imm = 0;
        self.init_maternally_imm = 0;
        self.init_recovery_imm = 0;
        
        
    def check_init(self):
        if self.param_beta_exp == 0 and self.param_beta_inf == 0:
            print('[ERROR] Both beta_exp and beta_inf cannot be zero.')
        elif self.param_beta_exp != 0 and self.param_beta_inf != 0:
            print('[ERROR] Both beta_exp and beta_inf cannot be non-zero.')
        else:
            print("[INFO] Initialization was done properly.")
        
node = Node()
node.check_init()
print(node.init_recovery_imm)