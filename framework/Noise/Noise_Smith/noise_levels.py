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
import numpy as np
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
def calculate_NOY(f, SPL):

    ## CORPO DA FUNÇÃO ##
    ## Tabelas para cálculo ##
    fref                = np.array([00050, 00063, 00080, 00100, 00125, 00160, 00200, 00250, 00315, 00400, 00500, 00630, 00800, 01000, 01250, 01600, 02000, 02500, 03150, 04000, 05000, 06300, 08000, 10000])
    SPLa                = [91.00, 85.90, 87.30, 79.90, 79.80, 76.00, 74.00, 74.90, 94.60, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 44.30, 50.70]
    SPLb                = [64.00, 60.00, 56.00, 53.00, 51.00, 48.00, 46.00, 44.00, 42.00, 40.00, 40.00, 40.00, 40.00, 40.00, 38.00, 34.00, 32.00, 30.00, 29.00, 29.00, 30.00, 31.00, 37.00, 41.00]
    SPLc                = [52.00, 51.00, 49.00, 47.00, 46.00, 45.00, 43.00, 42.00, 41.00, 40.00, 40.00, 40.00, 40.00, 40.00, 38.00, 34.00, 32.00, 30.00, 29.00, 29.00, 30.00, 31.00, 34.00, 37.00]
    SPLd                = [49.00, 44.00, 39.00, 34.00, 30.00, 27.00, 24.00, 21.00, 18.00, 16.00, 16.00, 16.00, 16.00, 16.00, 15.00, 12.00, 09.00, 05.00, 04.00, 05.00, 06.00, 10.00, 17.00, 21.00]
    SPLe                = [55.00, 51.00, 46.00, 42.00, 39.00, 36.00, 33.00, 30.00, 27.00, 25.00, 25.00, 25.00, 25.00, 25.00, 23.00, 21.00, 18.00, 15.00, 14.00, 14.00, 15.00, 17.00, 23.00, 29.00]
    Mb                  = [0.043478, 0.040570, 0.036831, 0.036831, 0.035336, 0.033333, 0.033333, 0.032051, 0.030675, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.029960, 0.029960, 0.029960, 0.029960, 0.029960, 0.029960, 0.029960, 0.042285, 0.042285]
    Mc                  = [0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.029960, 0.029960]
    Md                  = [0.079520, 0.068160, 0.068160, 0.059640, 0.053103, 0.053103, 0.053103, 0.053103, 0.053103, 0.053103, 0.053103, 0.053103, 0.053103, 0.053103, 0.059640, 0.053103, 0.053103, 0.047712, 0.047712, 0.053103, 0.053103, 0.068160, 0.079520, 0.059640]
    Me                  = [0.058098, 0.058098, 0.052288, 0.047534, 0.043573, 0.043573, 0.040221, 0.037349, 0.034859, 0.034859, 0.034859, 0.034859, 0.034859, 0.034859, 0.034859, 0.040221, 0.037349, 0.034859, 0.034859, 0.034859, 0.034859, 0.037349, 0.037349, 0.043573]
    ## Comparação das frequencias ##

    ## Definições dos loops ##
    a1                  = max(np.shape(f))
    a2 a3            = SPL.shape
    ## Eliminação dos pontos nã

    ## Conversão de SPL em NOY ##
    n = []
    for i2 in range(a2):
        for i1 in range(0,23)
            if SPL[i1,i2]>=SPLa[i1]:
                n[i1,i2] = 10^(Mc[i1]*(SPL[i1,i2]-SPLc[i1]))

            if (SPL[i1,i2]<SPLa[i1] and SPL[i1,i2]>=SPLb[i1]):
                n[i1,i2] = 10^(Mb[i1]*(SPL[i1,i2]-SPLb[i1]))

            if (SPL[i1,i2]<SPLb[i1] and SPL[i1,i2]>=SPLe[i1]):
                n[i1,i2] = 0.3*10^(Me[i1]*(SPL[i1,i2]-SPLe[i1]))

            if (SPL[i1,i2]<SPLe[i1] and SPL[i1,i2]>=SPLd[i1]):
                n[i1,i2] = 0.1*10^(Md[i1]*(SPL[i1,i2]-SPLd[i1]))

    ## DADOS DE SAIDA ##
    NOY                 = n

    return f, NOY


def calculate_PNL(f,NOY):
    ## CORPO DA FUNÇÃO ##
    ## Definições dos loops ##
    a1       = max(np.shape(f))
    a2,a3             = NOY.shape

    ## Conversão de NOY em PNdB##
    nmax = []
    N = []
    PNL = []
    for i2 in range(a3):
        for i1 in range(a1):
            nmax[i2]    = max(NOY[i2])
            N[i2]       = nmax[i2]+0.15*(np.sum(NOY[i2])-nmax[i2])
            PNL[i2]     = 40+10/np.log10(2)*np.log10(N[i2])


    return PNL


def calculate_PNLT(f,NOY):
    #step 1
    s = []
    for i1 in range(4,24):
        s[i1]           = SPL[i1]-SPL[i1-1]
    
    #step 2
    dels = []
    for i1 in range(1,3):
        dels[i1]        = 0
    
    for i1 = 5:24
        dels(i1)        = abs(s(i1)-s(i1-1))
    sc = []
    for i1 in range(1:24):
        sc[i1]          = 0
        if dels[i1]>5:
            sc[i1]      = 1
        
    
    #step 3
    SPLC = []
    for i1 in range(1,24):
        SPLC[i1]        = 0
        if sc[i1]==1:
            if s[i1]>0 and s[i1]>s[i1-1]:
                SPLC[i1] = 1
            
            if s[i1]<=0 and s[i1-1]>0:
                SPLC[i1-1] = 1
            
        
    
    #step 4
    SPLl = []
    for i1 in range(1,24):
        if SPLC[i1] != 1:
            SPLl[i1]    = SPL[i1]
        else:
            if i1<24:
                SPLl[i1] = 0.5*(SPL[i1-1]+SPL[i1+1])
            else:
                SPLl[i1] = SPL[i1]+s[i1]
            
        
    
    #step 5
    sl = []
    for i1 in range(4,24):
        sl[i1]          = SPLl[i1]-SPLl[i1-1]
    
    sl[3]               = sl[4]
    sl[25]              = sl[24]
    #step 6

    sabr = []
    for i1 in range(3,23):
        sbar[i1]        = 1/3*(sl[i1]+sl[i1+1]+sl[i1+2])
    
    #step 7
    SPLll = np.zeros(2)
    SPLll[2]            = SPL[3]
    for i1 in range(4,24):
        SPLll[i1)       = SPLll[i1-1]+sbar[i1-1]
    
    #step 8
    F = []
    for i1 in range(1:3):
        F[i1]           = 0
    
    for i1 in range(4,24):
        F[i1]           = 0
        if (SPL[i1]-SPLll[i1])>0:
            F[i1]       = SPL[i1]-SPLll[i1]
        
    

    ## Definição do valor da correção ##
    C = []
    for i1 in range(1,24):
        C[i1]           = 0
        if F[i1]>=1.5:
            if (f[i1]>=50 and f[i1]<500):
                if (F[i1] >= 1.5 and F[i1] < 3.0):
                    C[i1] = F[i1]/3-0.5
                
                if (F[i1] >= 3.0 and F[i1] < 20.0):
                    C[i1] = F[i1]/6
                
                if F[i1] >= 20.0:
                    C[i1] = 3+1/3
                
            
            if (f[i1]>=500 and f[i1]<5000):
                if (F[i1] >= 1.5 and F[i1] < 3.0):
                    C[i1] = 2*F[i1]/3-1.0
                
                if (F[i1] >= 3.0 and F[i1] < 20.0):
                    C[i1] = F[i1]/3
                
                if F[i1] >= 20.0:
                    C[i1] = 6+2/3
                
            
            if (f[i1]>=5000 and f[i1]<10000):
                if (F[i1] >= 1.5 and F[i1] < 3.0):
                    C[i1] = F[i1]/3-0.5
                
                if (F[i1] >= 3.0 and F[i1] < 20.0):
                    C[i1] = F[i1]/6
                
                if F[i1] >= 20.0:
                    C[i1] = 3+1/3
                
            
        
    


    ## DADOS DE SAIDA ##
    Cfin                = max(C)


    return Cfin

def calculate_EPNdB(tempo,PNLT):

    ## CORPO DA FUNÇÃO ##
    PNLTM               = max(PNLT)                                            # Determinação do PNLT máximo
    PNLTL               = PNLTM-10                                             # Determinação do nível mínimo a ser considerado
    
    a1                  = max(np.shape(PNLT))                                       # Determinação das variáveis de controle do cálculo
    dt                  = tempo[2]-tempo[1]                                    # Determinação das variáveis de controle do cálculo
    for i1=1:a1-1                                                               # Separação dos valores de PNLT que serão usados
        if PNLT(i1+1)>PNLTL and PNLT(i1)<PNLTL
            ind1        = i1+1
        else
            ind1        = 1

        if PNLT(i1+1)<PNLTL and PNLT(i1)>PNLTL
            ind2        = i1+1
        else
            ind2        = a1

    # Somatório do ruído
    termo1              = 0
    for i1=ind1:ind2
        termo1          = termo1+dt*10^(PNLT(i1)/10)

    D                   = 10*np.log10(0.1*termo1)-PNLTM-13                        # Determinação do fator de correção
    EPNdB               = PNLTM+D                                              # Determinação de EPNdB

    return EPNdB
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
