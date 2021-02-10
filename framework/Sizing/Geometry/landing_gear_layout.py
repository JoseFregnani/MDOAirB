"""
File name :
Author    : 
Email     : aarc.88@gmail.com
Date      : 
Last edit :
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - ROSKAM, J. Airplane Design vol. IV - Layout of landing gear and systems. DARCorp, 2010.
      TORENBEEK, E. Synthesis of subsonic airplane design. DUP / Kluwer, 1982.
Inputs:
    -
Outputs:
    -
TODO's:
    -

"""
# =============================================================================
# IMPORTS
# =============================================================================
import math
import numpy as np
from framework.Sizing.Geometry.tire_selection import tire_selection
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
global GRAVITY
GRAVITY = 9.80665
kgf_to_lbf = 2.204622622
ms_to_mph = 2.236936292
in_to_m = 0.0254
ft_to_m = 0.3048
rad_to_deg = 180/np.pi

def landing_gear_layout(vehicle):

    nose_landing_gear = vehicle['nose_langing_gear']
    main_landing_gear = vehicle['main_langing_gear']
    aircraft = vehicle['aircraft']
    fuselage = vehicle['fuselage']
    wing = vehicle['wing']
    
    # CÁLCULOS
    ns                  = 2                                                    # Número de struts do trem de pouso principal
    nt_m                = 2                                                    # Número de pneus por strut do trem principal
    nt_n                = 2                                                    # Número de pneus por strut do trem secundario
    psi_m               = main_landing_gear['pressure']                                           # Pressao maxima do pneu do TDP principal
    psi_n               = nose_landing_gear['pressure']                                               # Pressao maxima do pneu do TDP do nariz
    # DIMENSÕES PRIMÁRIAS
    ln                  = aircraft['forward_center_of_gravity_xposition'] - nose_landing_gear['xpostion']                           # Distância do tdp dianteiro ao CG [m]
    lm                  = main_landing_gear['xpostion']-aircraft['forward_center_of_gravity_xposition']                                 # Distância do tdp principal ao CG [m]
    M                   = main_landing_gear['xpostion']-aircraft['after_center_of_gravity_xposition'] 
    F                   = main_landing_gear['xpostion']-nose_landing_gear['xpostion']
    L                   = aircraft['forward_center_of_gravity_xposition'] - nose_landing_gear['xpostion']
    #
    Fator               = 1.07                                                # Fator de ajuste 14CFR25
    # wt                  = 3.658                                             # Razão de descida [m/s]

    ## CARGAS
    # Cargas estáticas
    OEW                 = 0.50*aircraft['maximum_takeoff_weight']
    
    #Pn_max              = OEW*(main_landing_gear['xpostion']-xcg_dianteiro)/F                         # Carga máxima no tdp dianteiro [kgf]
    fatrespdyn          = 2
    mi                  = 0.80 # coef de fricção
    J                   = aircraft['zCG'] + fuselage['width']/2 + main_landing_gear['piston_length'] + main_landing_gear['tyre_diameter']/2
    fatdyn              = fatrespdyn*mi*L*J/(F+mi*J)
    Pn_max              = OEW*((F-L)  + fatdyn)/F 
    #Pm_max              = OEW*(aircraft['after_center_of_gravity_xposition'] -nose_landing_gear['xpostion'])/F                          # Carga maxima no trem principal [kgf]
    Pm_max              = OEW*(F-M)/F 
    LoadMax             = Fator*(Pm_max*kgf_to_lbf)/(ns*nt_m)                    # Carga maxima por pneu no trem principal [lbf]
    if LoadMax > 59500:                                                       # Verifica carga máxima por pneu e acerta número de pneus
        nt_m_req        = math.ceil(LoadMax/59500)                                 # Define número de pneus requerido
        nwtest          = nt_m_req%ns                                     # Verifica se número requerido de pneus é multiplo de 4
        if nwtest != 0:
        #    disp('passei por aqui como?')
            nt_m        = (nwtest+1)*2                                        # Define número de pneus como um número par
        
    
    #fprintf('\n MLG: Tyre number per strut #2i \n',nt_m)
    
    # Cargas dinâmicas
    axg                 = 0.45
    Pn_dyn              = aircraft['maximum_takeoff_weight']*((lm+axg*aircraft['zCG'])/(lm+ln+axg*aircraft['zCG']))             # Carga no tdp dianteiro [kgf]
    # Carga por pneu
    TL_m_static         = LoadMax/kgf_to_lbf                                    # Carga estática por pneu no tdp principal [kgf]
    TL_n_static         = Pn_max/nt_n*Fator                                   # Carga estática por pneu no tdp dianteiro [kgf]
    TL_n_dyn            = 0                                                   # Carga dinâmica por pneu no tdp dianteiro [kgf]
    #
    MLW = aircraft['maximum_takeoff_weight']*0.9
    v_tfo               = 1.1*np.sqrt(2*aircraft['maximum_takeoff_weight']*GRAVITY/(1.225*aircraft['CL_maximum_takeoff']*wing['area']))  # Velocidade máxima de lift-off [m/s]
    v_land              = 1.2*np.sqrt(2*MLW*GRAVITY/(1.225*aircraft['CL_maximum_landing']*wing['area']))     # Velocidade máxima de toque no pouso [m/s]
    v_qualified         = max(v_tfo,v_land)                                   # Velocidade usada para dimensionamento dos pneus [m/s]
    ## PNEUS
    vqualmph            = v_qualified*ms_to_mph
    # Pneu tdp principal
    loadM               = TL_m_static*kgf_to_lbf
    #fprintf('\n Tyre sizing for main landing gear ... ')
    TDia, TWid = tire_selection(loadM,vqualmph,psi_m,'weight')
    print('\n Done! \n ')
    D0m_max             = TDia                                                 # Diâmetro máximo pneu tdp principal [m]
    #fprintf('\n MLF tyre diameter: #5.2f m \n', D0m_max)
    D0m_min             = 0.96*TDia                                            # Diâmetro mínimo pneu tdp principal [m]
    wm_max              = TWid                                                 # Largura máxima pneu tdp principal [m]
    mstatic_load        = 0.4*TDia                                             # Raio do pneu, carregado [m]
    st_m                = (0.25*(D0m_max+D0m_min)-(mstatic_load))              # Deflexão permitida do pneu [m]
    # Pneu tdp dianteiro (Tipo VII)
    loadN               = max([TL_n_static, TL_n_dyn])*kgf_to_lbf
    #fprintf('\n Tyre sizing for nose landing gear ... ')
    TDia, TWid = t= tire_selection(loadN,vqualmph,psi_n,'size')
    #fprintf('\n Done! \n ')
    D0n_max             = TDia                                                 # Diâmetro máximo pneu tdp dianteiro [m]
    D0n_min             = 0.96*TDia                                            # Diâmetro mínimo pneu tdp dianteiro [m]
    wn_max              = TWid                                                 # Largura máxima pneu tdp dianteiro [m]
    nstatic_load        = 0.4*TDia                                             # Raio do pneu, carregado [m]
    st_n                = ((D0n_max+D0n_min)/2/2-(nstatic_load))*in_to_m          # Deflexão permitida do pneu [m]
    ## SHOCK ABSORBERS (STRUTS)  - Mason
    ni_t                = 0.47                                                 # Eficiência para absorção de energia, pneu
    ni_s                = 0.8                                                  # Eficiência para absorção de energia, shock absorber (considerado como oleo-pneumático)
    Ng                  = 1.5                                                  # Fator de carga 14CFR25 [g]
    
    # TDP dianteiro
    vsink                = 10*ft_to_m
    Ss_n                = (0.5*Pn_max/GRAVITY*vsink**2/(1*(Pn_dyn)*Ng)-ni_t*st_n)/ni_s # Comprimento, shock absorber, tdp dianteiro [m]
    Ss_n                = Ss_n+1/12*in_to_m                                       # Comprimento de projeto, shock absorber, tdp dianteiro [m]
    ds_n                = (0.041+0.0025*(Pn_dyn/0.4535)**0.5)/3.28              # Diâmetro, shock absorber, tdp dianteiro [m]

    Lpist_n = Ss_n + 2.75*ds_n      
    nose_landing_gear['piston_length'] =  Lpist_n                               # MIL-L-8552 - Minimum piston length
    #fprintf('\n Nose landing gear Minimum piston length: #5.2f m \n',Lmain_landing_gear['piston_length'])
    # - TDP Principal
    
    # Energy calculation
    #  At takeoff
    vsink                = 6*ft_to_m                                              # Velocidade de descida (FAR)
    Sst_ma               = (0.50*vsink**2)/(ni_s*Ng*GRAVITY) - (ni_t*st_m)/ni_s       # Comprimento, shock absorber, tdp principal [m]
    Sst_ma               = Sst_ma+1/12*in_to_m                                    # Comprimento de projeto, shock absorber
    #  At landing
    vsink                = 10*ft_to_m
    Ssl_ma               = (0.50*vsink**2/(ni_s*Ng*GRAVITY) - ni_t*st_m)/ni_s         # Comprimento, shock absorber, tdp principal [m]
    Ssl_ma               = Ssl_ma+1/12*in_to_m                                    # Comprimento de projeto, shock absorber [m]
    
    Ss_m                 = max(Sst_ma, Ssl_ma)
    Pm                   = Pm_max/ns
    ds_m                 = (0.041+0.0025*(Pm/0.4535)**0.5)/3.28                 # Diâmetro, shock absorber, tdp principal [m]
    Lpist_m              = Ss_m + 2.75*ds_m                                    # MIL-L-8552 - Minimum piston length [m]
    main_landing_gear['piston_length'] = Lpist_m 
    #fprintf('\n Main landing gear Minimum piston length: #5.2f m \n',Lpist_m)
    ## ÂNGULOS
    # A (entre a vertical do tdp principal e o cg)
    A_min               = (np.arctan(M/aircraft['zCG']))*rad_to_deg                                  # valor para A mínimo [deg]
    A_max               = (np.arctan(lm/aircraft['zCG']))*rad_to_deg                                 # valor para A máximo [deg]
    # Beta (clearance da cauda com o solo)
    B                   = np.arctan((aircraft['zCG']-aircraft['zCG'])/(fuselage['length']-main_landing_gear['xpostion']))*rad_to_deg         
                                                                            # valor de beta
    return vehicle, A_min, nt_m,D0m_max, wm_max, Lpist_m, ds_m, Lpist_n, ds_n, wn_max, D0n_max
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
