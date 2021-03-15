"""
File name :
Author    : 
Email     : aarc.88@gmail.com
Date      : 
Last edit :
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    -
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

# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
def noise_engine():
    f = np.array([50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000])
    
    ## CORPO DA FUNÇÃO
    ## Dados da atmosfera ##
    atm                 = atmosfera(HP,DISA)                                   # propriedades da atmosfera
    Machd               = vairp/atm(7)                                         # Numero de Mach
    
    ## Dados do motor ##
    [FN,FF]             = motor(HP,Machd,ENGPAR(1),ENGPAR(2),ENGPAR(3),maneted,ENGPAR(5),ENGPAR(8))     # Atenção: N1 e N2
    
    ## Ruído do fan e compressor ##
    ratT                = engine3(8)/engine3(3)
    mponto              = engine5(2)
    nfan                = N1
    MTRd                = 1.3
    nrotor              = 38
    nstat               = 80
    RSS                 = 200
    IGV                 = 0
    [~, ruidoFant]      = Fan2(HP,DISA,RH,vairp,teta,fi,R,ENGPAR(5),ratT,mponto,nfan,MTRd,nrotor,nstat,RSS,IGV)
    
    
    ## Ruido da câmara de combustão ##
    mdot                = engine5(1)
    T3K                 = engine3(4)
    T4K                 = engine3(5)
    P3                  = engine2(4)
    RH                  = 70
    [~, ruidocamarat]  = Camaracomb(HP,DISA,RH,vairp,teta,fi,R,mdot,T3K,T4K,P3)
    
    
    ## Ruido da turbina ##
    Tturbsaida           = engine3(5)
    nturb                = N1
    MTRturb              = 0.50
    nrotor               = 76
    RSSturb              = 50
    [~, ruidoTurbinat]  = Turbina(HP,DISA,RH,vairp,teta,fi,R,mdot,nturb,Tturbsaida,MTRturb,nrotor,RSSturb)
    
    
    ## Ruido de Jato ##
    ACJ                 = engine4(2)
    ABJ                 = engine4(3)
    h                   = 0.150
    DCJ                 = 2*ACJ/(pi*h)+h/2
    VCJ                 = engine6(1)
    VBJ                 = engine6(2)
    TCJ                 = engine3(7)
    TBJ                 = engine3(8)
    roCJ                = 0.561
    roBJ                = 1.210
    plug                = 1.0
    coaxial             = 1.0
    [~, ruidoJatot]     = Bocal3(HP,DISA,RH,vairp,teta,fi,R,plug,coaxial,ACJ,ABJ,h,DCJ,VCJ,VBJ,TCJ,TBJ,roCJ,roBJ)
    
    
    ## Ruido total ##
    ruidoTotal          = 10*log10(10.^(0.1*ruidoFant)+10.^(0.1*ruidocamarat)+10.^(0.1*ruidoTurbinat)+10.^(0.1*ruidoJatot))
    
    
    ## DADOS DE SAIDA ##
    OASPLENG            = ruidoTotal
    ft                  = f
    
    return
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
