from time import time as tempo
import numpy as np
from numpy import tanh
from numba import njit, jit, vectorize
from numpy.lib.type_check import nan_to_num
import scipy.linalg as linalg


# PRECISÃO E DADOS INICIAIS

precisao_n = 0.0001
t = 1
n_0 = 1.0
mu_inicial = -2.0
tentativas_mu = 10000
tentativas_delta_limite = 100
precisao_delta = 0.000001
D_0 = 0.5
relax_occ = 0.5
relax_delt = 0.5

# Da pra simplificar muito o codigo, maioria das funções são leves modificações entre si

def obter_dado_T_e_J(Numeros, Temp, J, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M):
  
  t0 = tempo()  

  list_d = []
  list_n = []
  list_mu = []
  
  for num in Numeros:
    res = obter_dado_T_e_N([J], Temp, num, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M)
    list_d.append(res['deltas'][0])
    list_n.append(res['numeros'][0])
    list_mu.append(res['energia_quimica'][0])
    
  return {
    "tempo": tempo() - t0,
    "deltas": list_d,
    "numeros": list_n,
    "energia_quimica": list_mu
  }


def obter_dado_J_e_N(Temperaturas, n_med_esp, J, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M):
  t0 = tempo()  

  list_d = []
  list_n = []
  list_mu = []
  
  for Temp in Temperaturas:
    res = obter_dado_T_e_N([J], Temp, n_med_esp, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M)
    list_d.append(res['deltas'][0])
    list_n.append(res['numeros'][0])
    list_mu.append(res['energia_quimica'][0])
    
  return {
    "tempo": tempo() - t0,
    "deltas": list_d,
    "numeros": list_n,
    "energia_quimica": list_mu
  }
  
 
def obter_dado_T_e_N(Energias_Atracao_J, Temp, Numero_Med_Esp, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M):  
  inicio = tempo()
  
  list_d = []
  list_n = []
  list_mu = []
    
  for U in Energias_Atracao_J:

    # Resetar os valores para nova temperatura
    n.fill(n_0)
    D.fill(D_0)
    prom = np.zeros(2)
    dif = np.zeros(2)
    
    n_prom = n_0
    
    # resetar o mu_0
    mu_0 = mu_inicial
    
    # Obter mu_0
    for _ in range(tentativas_mu):
      error =  n_prom - Numero_Med_Esp
      mu_0 += 0.1 * error

      Potencial_Quimico.fill(mu_0)
      contador_delta = 0
      
      while ( contador_delta < tentativas_delta_limite ):
        
        contador_delta += 1
        
        # Resetar Matriz K e Delta
        K.fill(0.0)
        Delta.fill(0.0)
        
        construir_matriz_B(B, K, Delta, D, n, Potencial_Quimico, Dimensao, Sitios, U, t)  
        
        evals, evecs = linalg.eig(B)
        evecs = evecs.real
        evals = evals.real
        
        calcula_f(f,M,evals,Temp)
        
        # Resetando prom e dif
        prom[0] = 0.0
        prom[1] = 0.0
        dif[0] = 0.0
        dif[1] = 0.0
        
        calcular_parametros_occ_delt(f, n, D, evals, evecs, U, Dimensao, Sitios, prom, dif)  
        
        n_prom = prom[0]
        D_prom = prom[1]
        difn_prom = dif[0]
        difD_prom = dif[1]

        if abs(difD_prom) < precisao_delta:
          break
      
      if (abs(error) < precisao_n):
        break
    
    list_d.append(D_prom)
    list_n.append(n_prom)
    list_mu.append(mu_0)
    
  delta_tempo = tempo() - inicio  

  return {
    "tempo": delta_tempo,
    "deltas": list_d,
    "numeros": list_n,
    "energia_quimica": list_mu
  }
  

def obter_dado_T(Temp, Numeros, Energias_Atracao_J, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M):  
  t0 = tempo()
  
  Z_delta = []
  Z_numero = []
  Z_ener_quim = []
  
  for numero in Numeros:
    result = obter_dado_T_e_N(Energias_Atracao_J, Temp, numero, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M)
    Z_delta.append(result['deltas'])
    Z_numero.append(result['numeros'])
    Z_ener_quim.append(result['energia_quimica'])
    
  return {
    'Delta': np.array(Z_delta),
    'Numero': np.array(Z_numero),
    'Energia_Quimica': np.array(Z_ener_quim),
    'tempo': tempo() - t0
  }

def obter_dado_J(J, Numeros, Temperaturas, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M):  
  t0 = tempo()
  
  Z_delta = []
  Z_numero = []
  Z_ener_quim = []
  
  for numero in Numeros:
    
    delta = []
    num = []
    ener_quim = []
    
    for temp in Temperaturas: 

      result = obter_dado_T_e_N([J], temp, numero, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M)
      delta.append(result['deltas'][0])
      num.append(result['numeros'][0])
      ener_quim.append(result['energia_quimica'][0])
    
    Z_delta.append(delta)
    Z_numero.append(num)
    Z_ener_quim.append(ener_quim)
    
  return {
    'Delta': np.array(Z_delta),
    'Numero': np.array(Z_numero),
    'Energia_Quimica': np.array(Z_ener_quim),
    'tempo': tempo() - t0
  }
  
def obter_dado_N(Energias_Atracao_J, numero, Temperaturas, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M):  
  t0 = tempo()
  
  delta = []
  num = []
  ener_quim = []

  for temp in Temperaturas: 

    result = obter_dado_T_e_N(Energias_Atracao_J, temp, numero, n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M)
    delta.append(result['deltas'][0])
    num.append(result['numeros'][0])
    ener_quim.append(result['energia_quimica'][0])
  
    
  return {
    'Delta': np.array(delta),
    'Numero': np.array(num),
    'Energia_Quimica': np.array(ener_quim),
    'tempo': tempo() - t0
  }


# Modifica matriz D e n
@njit()
def calcular_parametros_occ_delt(f, n, D, evals, evecs, U, Dimensao, Sitios, prom, dif):
  for y in range(Dimensao):
    for x in range(Dimensao):
      
      indice = Dimensao * y + x
      occ = 0.0
      delt = 0.0
      
      for k in range(2 * Sitios):
        if evals[k] >= 0:
          occ += 2 * ( f[k] * (evecs[indice][k] ** 2) + (1.0 - f[k]) * (evecs[indice + Sitios][k] ** 2) )
          delt += U * (1.0 - 2*f[k]) * evecs[indice][k] * evecs[indice + Sitios][k]
      
      dif[0] += ((n[x][y] - occ)**2) / Sitios
      
      n[x][y] = (1.0 - relax_occ) * n[x][y] + relax_occ * occ
      
      dif[1] += ((D[x][y] - delt) ** 2) / Sitios
      
      D[x][y] = (1.0 - relax_delt) * D[x][y] + relax_delt * delt
      
      prom[0] += n[x][y] / Sitios 
      
      prom[1] += D[x][y] / Sitios


# Modificar f
@njit()
def calcula_f(f, M, evals, Temp):
  for k in range(M):
    f[k] = 0.5 * ( 1.0 - tanh(evals[k]/(2 * Temp)) ) 
    

@njit()
def construir_matriz_B(B, K, Delta, D, Numero, Potencial_Quimico, Dimensao, Sitios, U, t):
  # Modificar Matriz K e Delta
  for y in range(Dimensao):
    for x in range(Dimensao):
    
      indice = Dimensao * y + x
      
      K[indice][indice] = Potencial_Quimico[x][y] + 0.5 * U * Numero[x][y]
      Delta[indice][indice] = D[x][y]
      
      if y < Dimensao - 1:
        K[indice][indice + Dimensao] = -t   
        
      if x < Dimensao - 1:
        K[indice][indice + 1] = -t   
    
      if y >= 1:    
        K[indice][indice - Dimensao] = -t   
    
      if x >= 1:
        K[indice][indice - 1] = -t

  # Modificar Matriz B
  for x in range(Sitios):
    for y in range(Sitios):
      
      B[x][y] = K[x][y]
      B[x + Sitios][y + Sitios] = -K[x][y]
      B[x][y + Sitios] = Delta[x][y]
      B[x + Sitios][y] = Delta[x][y]

  
