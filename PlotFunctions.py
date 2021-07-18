import os
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# Pasta na qual são salvos o arquivo principal
pasta = 'resultados'

cwd = os.getcwd()
def plot3D(nomeX, X, nomeY, Y, nomeZ, Z, titulo='', show = True, visao_inicial=(31, -165), infimo=0, supremo=0):
  ax = plt.axes(projection='3d')
  ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')  
  ax.set_xlabel(nomeX)
  ax.set_ylabel(nomeY)
  ax.set_zlabel(nomeZ)
  ax.view_init(*visao_inicial)

  nome = f'{nomeX}x{nomeY}x{nomeZ} ' + titulo
  ax.set_title(nome)
  
  if infimo != supremo:
    ax.set_zlim(infimo, supremo)
  
  if show:  
    plt.get_current_fig_manager().set_window_title(nome)
    plt.show()
  else:
    data_hora = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    local = f"{cwd}/{pasta}/{nomeX}x{nomeY}x{nomeZ}"
    Path(local).mkdir(parents=True, exist_ok=True)
    plt.savefig(f'{local}/{data_hora}.png')
    
  plt.cla()


def plot2D(nomeX, X, nomeY, Y, titulo='', show = True, infimo=0, supremo=0):
  plt.plot(X, Y)
  plt.xlabel(nomeX)
  plt.ylabel(nomeY)
  nome = f'{nomeX}x{nomeY} ' + titulo
  plt.title(nome)
  
  if supremo != infimo:
    plt.ylim(infimo, supremo)
  
  if show:
    plt.get_current_fig_manager().set_window_title(nome)
    plt.show()
  else:
    data_hora = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    local = f"{cwd}/{pasta}/{nomeX}x{nomeY}"
    Path(local).mkdir(parents=True, exist_ok=True)
    plt.savefig(f'{local}/{data_hora}.png')
    
    
    