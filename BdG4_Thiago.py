#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 16:48:29 2021.

O programa pega um Grid N x N, representando em cada ponto átomos. 
O intuito é incluir a influência de cada ponto para calcular o Δ e o µ, utilizando as equações de Bogoliubov de Gennes. 
O programa tem como objetivo plotar e/ou salvar gráficos relacionando as diversas variáveis em questão.

@author: Thiago Oliveira Jucá Vasconcelos
"""  
  
import numpy as np
import winsound
from PlotFunctions import plot3D, plot2D # Contem as funções que farão o plot, como também o nome da pasta onde será salvas as imagens
from CalcFunctions import obter_dado_J_e_N, obter_dado_T_e_J, obter_dado_T_e_N, obter_dado_T, obter_dado_J, obter_dado_N # Contem as funções que calculam valores requisitados e os parametros iniciais e de precisão
from PergFunctions import Perguntas # Contém as perguntas feitas antes de iniciar o cálculo

# Falta implementar previsão de tempo(se tu testar uma vez, saberá mais ou menos quanto tempo)
# Seria interessante tentar juntar com Multiprocessing
pos_virgula = 2
subir_graf_do_max = 0.1

def main():
  
  dados = Perguntas()
  
  som_iniciar()
  print("Iniciando o calculo! \n")
  
  # Inicializando Constantes
  Dimensao = dados['dimensao']
  Sitios = Dimensao * Dimensao
  M = 2 * Sitios
  
  # Grids utilizados
  Potencial_Quimico = np.zeros((Dimensao, Dimensao))
  Delta = np.zeros((Sitios, Sitios))
  
  f = np.zeros(M)
  n = np.zeros((Dimensao, Dimensao))
  D = np.zeros((Dimensao, Dimensao))
  B = np.zeros((M,M))
  K = np.zeros((Sitios, Sitios))  
  
  if dados['tipo_plot'] == '2d':
   
    if dados['variavel'] == 't':
      resultado = obter_dado_J_e_N(dados['intervalo'], dados['numero'], dados['energia_atrativa'], n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M, dados['aleatoridade']['aleatoridade'], dados['aleatoridade']['valor'])
      plot2D('T', dados['intervalo'], 'Δ', resultado['deltas'], f'com n = {dados["numero"]} e J = {dados["energia_atrativa"]}', show=dados['display'])
      plot2D('T', dados['intervalo'], 'µ', resultado['energia_quimica'], f'com n = {dados["numero"]} e J = {dados["energia_atrativa"]}', show=dados['display'])
      # Para verificar precisão pode tambem plotar resultado['numeros'] é pra ser cte, mas na pratica a conta se baseia em aproximar ao maximo dele
      
    elif dados['variavel'] == 'j':
      resultado = obter_dado_T_e_N(dados['intervalo'], dados['temperatura'], dados['numero'], n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M, dados['aleatoridade']['aleatoridade'], dados['aleatoridade']['valor'])
      plot2D('J', dados['intervalo'], 'Δ', resultado['deltas'], f'com n = {dados["numero"]} e T = {dados["temperatura"]}K', show=dados['display'])
      plot2D('J', dados['intervalo'], 'µ', resultado['energia_quimica'], f'com n = {dados["numero"]} e T = {dados["temperatura"]}K', show=dados['display'])
      # Para verificar precisão pode tambem plotar resultado['numeros'] é pra ser cte, mas na pratica a conta se baseia em aproximar ao maximo dele
    elif dados['variavel'] == 'a':
      resultado = {'array': [], 'tempo': 0}
      for v in dados['intervalo']:
        res = obter_dado_J_e_N([dados['temperatura']], dados['numero'], dados['energia_atrativa'], n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M, True, v)
        resultado['array'].append(res['deltas'][0])
        resultado['tempo'] += res['tempo']
      plot2D('v', dados['intervalo'] , 'Δ', resultado['array'], f'com n = {dados["numero"]}, J = {dados["energia_atrativa"]}eV e T = {dados["temperatura"]}K', show=dados['display'], infimo=0, supremo=(max(resultado['array'])+subir_graf_do_max))
    
    else:
      resultado = obter_dado_T_e_J(dados['intervalo'], dados['temperatura'], dados['energia_atrativa'], n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M, dados['aleatoridade']['aleatoridade'], dados['aleatoridade']['valor'])
      plot2D('n', dados['intervalo'], 'Δ', resultado['deltas'], f'com J = {dados["energia_atrativa"]} e T = {dados["temperatura"]}K', show=dados['display'])
      plot2D('n', dados['intervalo'], 'µ', resultado['energia_quimica'], f'com J = {dados["energia_atrativa"]}eV e T = {dados["temperatura"]}K', show=dados['display'])
      # Para verificar precisão pode tambem plotar resultado['numeros'] é pra ser uma reta crescente, mas na pratica a conta se baseia em aproximar ao maximo dele
  
  else:
   
    if dados['constante'] == 't':
      X, Y = np.meshgrid(dados['intervalo_energia_atrativa'], dados['intervalo_numero'])
      resultado = obter_dado_T(dados['Temperatura'], dados['intervalo_numero'], dados['intervalo_energia_atrativa'], n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M, dados['aleatoridade']['aleatoridade'], dados['aleatoridade']['valor'])
      plot3D('J', X, 'n', Y, 'Δ', np.array(resultado['Delta']), f' com T = {dados["Temperatura"]}K', show=dados['display'])
      plot3D('J', X, 'n', Y, 'µ', np.array(resultado['Energia_Quimica']), f' com T = {dados["Temperatura"]}K', show=dados['display'])
      # Para verificar precisão pode tambem plotar resultado['numeros'] é pra ser um plano, mas na pratica a conta se baseia em aproximar ao maximo dele
      
    elif dados['constante'] == 'j':
      X, Y = np.meshgrid(dados['intervalo_temperatura'], dados['intervalo_numero'])
      resultado = obter_dado_J(dados['Energia Atrativa'], dados['intervalo_numero'], dados['intervalo_temperatura'], n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M, dados['aleatoridade']['aleatoridade'], dados['aleatoridade']['valor'])
      plot3D('T', X, 'n', Y, 'Δ', np.array(resultado['Delta']), f' com J = {dados["Energia Atrativa"]}eV', show=dados['display'])
      plot3D('T', X, 'n', Y, 'µ', np.array(resultado['Energia_Quimica']), f' com J = {dados["Energia Atrativa"]}eV', show=dados['display'])
      # Para verificar precisão pode tambem plotar resultado['numeros'] é pra ser um plano, mas na pratica a conta se baseia em aproximar ao maximo dele
    
    else:
      X, Y = np.meshgrid(dados['intervalo_energia_atrativa'], dados['intervalo_temperatura'])
      resultado = obter_dado_N(dados['intervalo_energia_atrativa'], dados['Número'], dados['intervalo_temperatura'], n, D, Potencial_Quimico, B, K, Delta, Dimensao, Sitios, f, M, dados['aleatoridade']['aleatoridade'], dados['aleatoridade']['valor'])  
      plot3D('J', X, 'T', Y, 'Δ', np.array(resultado['Delta']), f' com n = {dados["Número"]}', show=dados['display'])
      plot3D('J', X, 'T', Y, 'µ', np.array(resultado['Energia_Quimica']), f' com n = {dados["Número"]}', show=dados['display'])
      # Para verificar precisão pode tambem plotar resultado['numeros'] é pra ser um plano, mas na pratica a conta se baseia em aproximar ao maximo dele
    
  print("\033[92mTempo de execução = ", round(resultado['tempo'], pos_virgula), "s\033[0m")
  som_alertar()


def som_alertar():
  for x in range(3):
    winsound.Beep(500-100*x, 200)
  for x in range(2):
    winsound.Beep(200+200*x, 200)
    
  
def som_iniciar():
  for x in range(4):
    winsound.Beep(250+50*x, 80 + 10 * x)

if __name__ == '__main__':
  main()