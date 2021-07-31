import sys
import os
from time import sleep
from numba.core.types.functions import RecursiveCall
from numpy import linspace

# O codigo podia está mais simplificado, usando um decorador de pergunta, reduziria muito o tamanho do código 

TEMPO_OCIO = 0.15
class cores:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'


def Perguntas():
    resultado = {}
    
    LimparTerminal(0, False)
    resultado['dimensao'] = ObterDimensao()
    
    tipo_plot = ObterTipoPrint()
    resultado['tipo_plot'] = tipo_plot
    
    if tipo_plot == '2d':
        variavel = ObterVariavel()
        resultado['variavel'] = variavel
        
        resultado['intervalo'] = ObterIntervalo(variavel)
         
        if variavel != 't':
            resultado['temperatura'] = ObterConstante('Temperatura')
        if variavel != 'n':
            resultado['numero'] = ObterConstante('Número')
        if variavel != 'j':
            resultado['energia_atrativa'] = ObterConstante('Energia Atrativa')
        if variavel != 'a':
            resultado['aleatoridade'] = ObterAleatoridade()
            
    else:
        constante = ObterValorFixo()
        resultado['constante'] = constante
        
        nome_constante = 'Temperatura' if constante == 't' else ('Número' if constante == 'n' else 'Energia Atrativa')
        resultado[nome_constante] = ObterConstante(nome_constante)
        
        if constante != 't':
            resultado['intervalo_temperatura'] = ObterIntervalo('t')
        if constante != 'n':
            resultado['intervalo_numero'] = ObterIntervalo('n')
        if constante != 'j':
            resultado['intervalo_energia_atrativa'] = ObterIntervalo('j')
 
        resultado['aleatoridade'] = ObterAleatoridade()
    
    
    resultado['display'] = ObterEstiloDisplay()
        
    return resultado
    

def DecoradorLembrete(funcao):
    def Wrapper(*args, **kwargs):
        print(f'{cores.OKGREEN}\n(PRECIONE CTRL + C PARA TERMINAR O PROGRAMA A QUALQUER MOMENTO)\n{cores.ENDC}')
        return funcao(*args, **kwargs)
    
    return Wrapper

@DecoradorLembrete
def ObterDimensao():
    while (True):
        try:
            dimensao = int(input('Qual é a dimensão da rede que gostaria de analisar?\n\n=> '))
            if dimensao <= 0:
                raise
            break
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('A dimensão da rede necessita ser um número inteiro positivo...\n')
    
    LimparTerminal(printar=False)
    return dimensao


@DecoradorLembrete
def ObterTipoPrint():
    while (True):
        try:
            tipo_plot = input('Qual tipo de plot pretende obter? (2D/3D)\n\n=> ').lower()
            
            if tipo_plot in ['2d', '3d']:
                break
            raise
            
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('O gráfico obtido pode ser 2D ou 3D...\n')
    
    LimparTerminal(printar=False)
    return tipo_plot

@DecoradorLembrete
def ObterAleatoridade():
    while (True):
        try:
            aleatoridade = input('Gostaria de incluir aleatoridade? (s,n)\n\n=> ').lower()
            
            if aleatoridade in ['s', 'n']:
                if aleatoridade == 's':
                    aleatoridade = True
                    valor = input('\nQual é a constante de proporcionalidade para aleatoridade? (default 1 por exemplo)\n\n=> ')
                    try:
                        valor = int(valor)
                    except:
                        valor = 1
                    break
                aleatoridade = False
                valor = 1
                break
            raise
            
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('Por favor escreva s ou n!\n')
    
    LimparTerminal(printar=False)
    return {'aleatoridade': aleatoridade, 'valor': valor}

@DecoradorLembrete
def ObterVariavel():
    while (True):
        try:
            variavel = input('Qual será a variável que pretende por em análise? (T, n, J, a)\n\n=> ').lower()
            
            if variavel in ['t', 'n', 'j', 'a']:
                break
            raise
            
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('Para Graficos 2D é necessário definir uma variável. Podendo ser Temperatura(T), Número(n), Energia Atrativa(J), Aleatoria(a)...\n')
    
    LimparTerminal(printar=False)
    return variavel

@DecoradorLembrete
def ObterValorFixo():
    while (True):
        try:
            variavel = input('Qual será a constante que pretende por em análise? (T, n, J)\n\n=> ').lower()
            
            if variavel in ['t', 'n', 'j']:
                break
            raise
            
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('Para Graficos 3D é necessário definir uma constante. Podendo ser Temperatura(T), Número(n) ou Energia Atrativa(J)...\n')
    
    LimparTerminal(printar=False)
    return variavel


@DecoradorLembrete
def ObterIntervalo(variavel):
    
    nome_variavel = 'Temperatura' if variavel == 't' else ('Número' if variavel == 'n' else ('Energia Atrativa' if variavel == 'j' else 'Aleatoriedade'))
    while (True):
        try:
            inicial = float(input(f'Qual será o valor inicial da {nome_variavel}? (em Kelvin)\n\n=> '))
            
            if inicial < 0:
                raise
            elif nome_variavel == 'Número' and inicial > 2:    
                raise
            
            final = float(input(f'\nQual será o valor final da {nome_variavel}? (em Kelvin)\n\n=> '))
            
            if final < 0:
                raise
            elif nome_variavel == 'Número' and final > 2:    
                raise
            elif final <= inicial:
                raise
            break
            
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('Escolha um numero positivo, com inicial sendo menor que o final...\n')
            if nome_variavel == 'Número':
                PrintAviso('O Número pode ser apenas entre 0 e 2...\n')
    
    
    LimparTerminal()            
    while (True):
        try:
            divisoes = int(input(f'Qual será o tamanho da partição da {nome_variavel}? \n\n=> '))
            
            if divisoes <= 0:
                raise
            break
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('Escolha um numero inteiro positivo...\n')
    
    LimparTerminal(printar=False)
    return linspace(inicial, final, divisoes)


@DecoradorLembrete
def ObterConstante(nome_constante):
    while (True):
        try:
            constante = float(input(f'Qual será o valor para {nome_constante}? \n\n=> '))
            
            if constante < 0:
                raise
            elif nome_constante == 'Número' and constante > 2:
                raise
            break
            
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('Escolha um numero inteiro positivo...\n')
            if nome_constante == 'Número':
                PrintAviso('O Número pode ser apenas entre 0 e 2...\n')
    
    LimparTerminal(printar=False)
    return constante


@DecoradorLembrete
def ObterEstiloDisplay():
    while (True):
        try:
            
            resposta = input(f'Como gostaria de receber arquivo?\n\na) Salvar {cores.OKGREEN}(para trocar o nome do diretorio, modifique a constante global em PlotFunctions.py){cores.ENDC}\n\nb) Mostrar\n\n=> ').lower()
            if resposta[0] in ['a', 'b']:
                break
            raise
        except KeyboardInterrupt:
            DesligarPrograma()
        except:
            LimparTerminal()
            PrintAviso('Escolha uma das letras: "a" ou "b"...\n')
    
    LimparTerminal(printar=False)
    display = True if resposta[0] == 'b' else False
    return display

def LimparTerminal(t=TEMPO_OCIO, printar=True):
    sleep(t)
    os.system('cls||clear')
    if printar:
        print(f'{cores.OKGREEN}\n(PRECIONE CTRL + C PARA TERMINAR O PROGRAMA A QUALQUER MOMENTO)\n{cores.ENDC}')


def DesligarPrograma():
    print('\nTerminando...\n')
    LimparTerminal(printar=False)
    sys.exit()
    

def PrintAviso(aviso):
    print(f'{cores.WARNING}{aviso}{cores.ENDC}')

# Debug perguntas
if __name__ == '__main__':
    print(Perguntas())