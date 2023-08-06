# -*- coding: utf-8 -*-
'''
EXPOsan: Exposition of sanitation and resource recovery systems

This module is developed by:
    
    Joy Zhang <joycheung1994@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/EXPOsan/blob/main/LICENSE.txt
for license details.
'''

import numpy as np
import qsdsan as qs
from qsdsan import sanunits as su, processes as pc, WasteStream, System
from qsdsan.utils import time_printer, ospath
from chemicals.elements import molecular_weight as get_mw
from exposan.metab_mock import DegassingMembrane as DM, METAB_AnCSTR as AB

folder = ospath.dirname(__file__)

__all__ = (
    'create_systems', 
    'default_inf_concs',
    'default_R1_init_conds',
    'default_R2_init_conds',
    'R1_ss_conds',
    'R2_ss_conds',
    'yields_bl', 'mus_bl', 'Ks_bl',
    'biomass_IDs'
    )

#%% default values
Q = 5           # influent flowrate [m3/d]
T1 = 273.15+35  # temperature [K]
Vl1 = 5         # liquid volume [m^3]
Vg1 = 0.556     # headspace volume [m^3]
split_1 = 0.75  # split ratio to side-stream
tau_1 = 0.021   # degassing membrane retention time [d]

T2 = 273.15+25    
Vl2 = 75
Vg2 = 5
split_2 = 0.75
tau_2 = 0.021

fermenters = ('X_su', 'X_aa', 'X_fa', 'X_c4', 'X_pro')
methanogens = ('X_ac', 'X_h2')
biomass_IDs = (*fermenters, *methanogens)

C_mw = get_mw({'C':1})
N_mw = get_mw({'N':1})

default_inf_concs = {
    'S_su':3.0,
    'S_aa':0.6,
    'S_fa':0.4,
    'S_va':0.4,
    'S_bu':0.4,
    'S_pro':0.4,
    'S_ac':0.4,
    'S_h2':5e-9,
    'S_ch4':5e-6,
    'S_IC':0.04*C_mw,
    'S_IN':0.01*N_mw,
    'S_I':0.02,
    'X_c':0.1,
    'X_ch':0.3,
    'X_pr':0.5,
    'X_li':0.25,
    'X_aa':1e-3,
    'X_fa':1e-3,
    'X_c4':1e-3,
    'X_pro':1e-3, 
    'X_ac':1e-3, 
    'X_h2':1e-3, 
    'X_I':0.025, 
    'S_cat':0.04, 
    'S_an':0.02
    }

yields_bl = {
         'Y_su': 0.1,
         'Y_aa': 0.08,
         'Y_fa': 0.06,
         'Y_c4': 0.06,
         'Y_pro': 0.04,
         'Y_ac': 0.05,
         'Y_h2': 0.06
         }

mus_bl = np.array([5.0e-01, 1.0e+01, 1.0e+01, 1.0e+01, 3.0e+01, 5.0e+01, 6.0e+00,
                   2.0e+01, 2.0e+01, 1.3e+01, 8.0e+00, 3.5e+01, 2.0e-02, 2.0e-02,
                   2.0e-02, 2.0e-02, 2.0e-02, 2.0e-02, 2.0e-02])

Ks_bl = np.array([5.0e-01, 3.0e-01, 4.0e-01, 2.0e-01, 
                  2.0e-01, 1.0e-01, 1.5e-01, 7.0e-06])

default_R1_init_conds = {
    'S_su': 0.0124*1e3,
    'S_aa': 0.0055*1e3,
    'S_fa': 0.1074*1e3,
    'S_va': 0.0123*1e3,
    'S_bu': 0.0140*1e3,
    'S_pro': 0.0176*1e3,
    'S_ac': 0.0893*1e3,
    'S_h2': 2.5055e-7*1e3,
    'S_ch4': 0.0555*1e3,
    'S_IC': 0.0951*C_mw*1e3,
    'S_IN': 0.0945*N_mw*1e3,
    'S_I': 0.1309*1e3,
    'X_ch': 0.0205*1e3,
    'X_pr': 0.0842*1e3,
    'X_li': 0.0436*1e3,
    'X_su': 1.87*1e3,
    'X_aa': 5.58*1e3,
    'X_fa': 2.03*1e3,
    'X_c4': 2.15*1e3,
    'X_pro': 1.00*1e3,
    }

default_R2_init_conds = {
    'S_su': 0.0124*1e3,
    'S_aa': 0.0055*1e3,
    'S_fa': 0.1074*1e3,
    'S_va': 0.0123*1e3,
    'S_bu': 0.0140*1e3,
    'S_pro': 0.0176*1e3,
    'S_ac': 0.0893*1e3,
    'S_h2': 2.5055e-7*1e3,
    'S_ch4': 0.0555*1e3,
    'S_IC': 0.0951*C_mw*1e3,
    'S_IN': 0.0945*N_mw*1e3,
    'S_I': 0.1309*1e3,
    'X_ac': 8.80*1e3,
    'X_h2': 3.70*1e3,
    }

R1_ss_conds = {
    'S_su': 0.0145871088552909*1e3,
    'S_aa': 0.00643308564144693*1e3,
    'S_fa': 0.634823005990967*1e3,
    'S_va': 0.624510322247682*1e3,
    'S_bu': 1.03793927591996*1e3,
    'S_pro': 1.24676871525373*1e3,
    'S_ac': 2.00250371674824*1e3,
    'S_h2': 0.00850364943532684*1e3,
    'S_ch4': 0.0000422133982597226*1e3,
    'S_IC': 0.0951*C_mw*1e3,
    'S_IN': 0.0945*N_mw*1e3,
    'S_I': 0.027310256066728*1e3,
    'X_c': 0.146203507058736*1e3,
    'X_ch': 0.0286018513139117*1e3,
    'X_pr': 0.0467836694957302*1e3,
    'X_li': 0.0247209587890493*1e3,
    'X_su': 4.69052782535406*1e3,
    'X_aa': 1.22829926704024*1e3,
    'X_fa': 0.0147446263753011*1e3,
    'X_c4': 0.0149933579422897*1e3,
    'X_pro': 0.0145343147735253*1e3,
    'X_ac': 0.00098041337766024*1e3,
    'X_h2': 0.00110808891184369*1e3,
    'X_I': 0.0396205121367899*1e3
    }

R2_ss_conds = {
    'S_su': 0.00106990968535691*1e3,
    'S_aa': 0.00125571416517827*1e3,
    'S_fa': 0.121097573221394*1e3,
    'S_va': 0.0132519103137696*1e3,
    'S_bu': 0.0172912281196732*1e3,
    'S_pro': 0.020032163173878*1e3,
    'S_ac': 0.00574002755366853*1e3,
    'S_h2': 3.76969944940856e-08*1e3,
    'S_ch4': 0.0499411746585487*1e3,
    'S_IC': 0.0951*C_mw*1e3,
    'S_IN': 0.0945*N_mw*1e3,
    'S_I': 0.105601391746794*1e3,
    'X_c': 0.0897520281015078*1e3,
    'X_ch': 0.00108163641708242*1e3,
    'X_pr': 0.00120204580901502*1e3,
    'X_li': 0.00150204523369107*1e3,
    'X_su': 0.195961987850137*1e3,
    'X_aa': 0.059723477130333*1e3,
    'X_fa': 0.0351858744892462*1e3,
    'X_c4': 0.0812315951844566*1e3,
    'X_pro': 0.0503466475437059*1e3,
    'X_ac': 1.1653549028287*1e3,
    'X_h2': 0.4352809013846*1e3,
    'X_I': 0.196117291164614*1e3
    }


# %%
# =============================================================================
# Preliminary analyses with mock METAB configuration
# =============================================================================

def create_systems(flowsheet_A=None, flowsheet_B=None, flowsheet_C=None,
                   inf_concs={}, R1_init_conds={}, R2_init_conds={}):
    flowsheet_A = flowsheet_A or qs.Flowsheet('METAB_sysA')
    qs.main_flowsheet.set_flowsheet(flowsheet_A)
    
    ############# load components and set thermo #############
    pc.create_adm1_cmps()

    ############# create WasteStream objects #################
    inf_concs = inf_concs or default_inf_concs
    brewery_ww = WasteStream('BreweryWW_A', T=T1)
    brewery_ww.set_flow_by_concentration(Q, concentrations=inf_concs, units=('m3/d', 'kg/m3'))
    eff_A = WasteStream('Effluent_A', T=T2)
    bg1_A = WasteStream('biogas_1A', phase='g')
    bg2_A = WasteStream('biogas_2A', phase='g')
    
    ############# load process model ###########################
    adm1 = pc.ADM1()
    
    ############# sysA unit operation ########################   
    H2E = AB('H2E', ins=[brewery_ww, 'return_1'], outs=('sidestream_1', ''), 
            split=(split_1, 1-split_1), V_liq=Vl1, V_gas=Vg1, T=T1, model=adm1, 
            retain_cmps=fermenters)
    DM1 = DM('DM1', ins=H2E-0, outs=(bg1_A, 1-H2E), tau=tau_1)
    CH4E = AB('CH4E', ins=[H2E-1, 'return_2'], outs=('sidestream_2', eff_A), 
            split=(split_2, 1-split_2), V_liq=Vl2, V_gas=Vg2, T=T2, model=adm1,
            retain_cmps=methanogens)
    DM2 = DM('DM2', ins=CH4E-0, outs=(bg2_A, 1-CH4E), tau=tau_2)
    H2E.set_init_conc(**R1_ss_conds)
    CH4E.set_init_conc(**R2_ss_conds)
    # H2E.set_init_conc(**R1_init_conds)
    # CH4E.set_init_conc(**R2_init_conds)
    sysA = System('mock_METAB', 
                  path=(H2E, DM1, CH4E, DM2),
                  recycle=(DM1-1, DM2-1))
    sysA.set_dynamic_tracker(H2E, CH4E, bg1_A, bg2_A)
    
    #***************************************************
    flowsheet_B = flowsheet_B or qs.Flowsheet('METAB_sysB')
    qs.main_flowsheet.set_flowsheet(flowsheet_B)

    ############# sysB streams ########################
    inf_b = brewery_ww.copy('BreweryWW_B')
    eff_B = WasteStream('Effluent_B', T=T2)
    bg1_B = WasteStream('biogas_1B', phase='g')
    bg2_B = WasteStream('biogas_2B', phase='g')
    
    ############# sysB unit operation #################
    R1_init_conds = R1_init_conds or default_R1_init_conds
    R2_init_conds = R2_init_conds or default_R2_init_conds
    AnR1 = su.AnaerobicCSTR('AnR1', ins=inf_b, outs=(bg1_B, ''), 
                            V_liq=Vl1, V_gas=Vg1, T=T1, model=adm1, 
                            retain_cmps=fermenters)
    AnR2 = su.AnaerobicCSTR('AnR2', ins=AnR1-1, outs=(bg2_B, eff_B), 
                            V_liq=Vl2, V_gas=Vg2, T=T2, model=adm1,
                            retain_cmps=methanogens)
    # AnR1.set_init_conc(**R1_init_conds)
    # AnR2.set_init_conc(**R2_init_conds)
    AnR1.set_init_conc(**R1_ss_conds)
    AnR2.set_init_conc(**R2_ss_conds)
    sysB = System('baseline', path=(AnR1, AnR2))
    sysB.set_dynamic_tracker(AnR1, AnR2, bg1_B, bg2_B)
    
    #***************************************************
    flowsheet_C = flowsheet_C or qs.Flowsheet('METAB_sysC')
    qs.main_flowsheet.set_flowsheet(flowsheet_C)
    
    ############# sysC streams ########################
    inf_c = brewery_ww.copy('BreweryWW_C')
    eff_c = WasteStream('Effluent_C', T=T2)
    bgm1 = WasteStream('biogas_mem_1', phase='g')
    bgm2 = WasteStream('biogas_mem_2', phase='g')
    bgh1 = WasteStream('biogas_hsp_1', phase='g')
    bgh2 = WasteStream('biogas_hsp_2', phase='g')
    
    ############# sysC unit operation #################
    sc1 = 0.1
    sc2 = 0.1
    R1 = su.AnaerobicCSTR('R1', ins=[inf_c, 'return_1'], 
                          outs=(bgh1, 'sidestream_1', ''), 
                          split=(sc1, 1-sc1),
                          V_liq=Vl1, V_gas=Vg1, T=T1, model=adm1, 
                          retain_cmps=fermenters)
    DM1c = DM('DM1_c', ins=R1-1, outs=(bgm1, 1-R1), tau=tau_1)
    # DM1c = DM('DM1_c', ins=R1-1, outs=(bgm1, 1-R1), tau=0.1)    

    R2 = su.AnaerobicCSTR('R2', ins=[R1-2, 'return_2'], 
                          outs=(bgh2, 'sidestream_2', eff_c), 
                          split=(sc2, 1-sc2),
                          V_liq=Vl2, V_gas=Vg2, T=T2, model=adm1,
                          retain_cmps=methanogens)
    DM2c = DM('DM2_c', ins=R2-1, outs=(bgm2, 1-R2), tau=tau_2)
    # DM2c = DM('DM2_c', ins=R2-1, outs=(bgm2, 1-R2), tau=0.1)
    R1.set_init_conc(**R1_ss_conds)
    R2.set_init_conc(**R2_ss_conds)
    sysC = System('combined_METAB', path=(R1, DM1c, R2, DM2c),
                  recycle=(DM1c-1, DM2c-1))
    sysC.set_dynamic_tracker(R1, R2, bgm1, bgm2, bgh1, bgh2)
              
    return sysA, sysB, sysC

#%%
@time_printer
def run(t, t_step, method=None, **kwargs):
    global sysA, sysB, sysC
    sysA, sysB, sysC = create_systems()
    print(f'Simulating {sysA.ID}...')
    sysA.simulate(state_reset_hook='reset_cache',
                  t_span=(0,t),
                  t_eval=np.arange(0, t+t_step, t_step),
                  method=method,
                  # export_state_to=ospath.join(folder, f'results/{method}_{t}d_sysA.xlsx'),
                  **kwargs)
    print(f'Simulating {sysB.ID}...')
    sysB.simulate(state_reset_hook='reset_cache',
                  t_span=(0,t),
                  t_eval=np.arange(0, t+t_step, t_step),
                  method=method,
                  # export_state_to=ospath.join(folder, f'results/{method}_{t}d_sysB.xlsx'),
                  **kwargs)
    print(f'Simulating {sysC.ID}...')
    sysC.simulate(state_reset_hook='reset_cache',
                  t_span=(0,t),
                  t_eval=np.arange(0, t+t_step, t_step),
                  method=method,
                  # export_state_to=ospath.join(folder, f'results/{method}_{t}d_sysB.xlsx'),
                  **kwargs)

if __name__ == '__main__':
    t = 120
    t_step = 3
    # method = 'RK45'
    # method = 'RK23'
    # method = 'DOP853'
    # method = 'Radau'
    method = 'BDF'
    # method = 'LSODA'
    msg = f'Method {method}'
    print(f'\n{msg}\n{"-"*len(msg)}') # long live OCD!
    print(f'Time span 0-{t}d \n')
    run(t, t_step, method=method)