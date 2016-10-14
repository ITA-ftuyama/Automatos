# -*- coding: cp1252 -*-
#
#       Simulador da Máquina de Turing    
#   
#  Autor: Felipe Tuyama     
import copy
import sys

# Nó de Transição
class Transition(object):
    def __init__(self, st2, RD, WR, DIR):
        self.st = st2
        self.RD = RD
        self.WR = WR
        if DIR == 'L':
            self.DIR = -1
        else: self.DIR = 1
        
# Leitura da Transição da MT
def nextData(char):
    global reader
    begin = 0
    while begin < len(reader) and reader[begin] != char: 
        begin += 1
    if begin == 0: info = ""
    else: info = reader[0:begin]
    reader = reader[begin+1:len(reader)]
    return info

# Leitura de uma linha não vazia sem \n
def read():
    lido = arquivo.readline().rstrip('\n')
    while lido == "":
        lido = arquivo.readline().rstrip('\n')
    return lido

# Leitura do Arquivo de Entrada especificando MT
def readMT():
    global reader
    for i in range(0, 4):
        reader = " "
        while reader[0] != '#':
            reader = read()
        reader = read()
        while reader[0] != '#':
            if i == 0:   alphabet.append(reader)
            elif i == 1:
                for j in range(0, int(reader)):
                    TFE.append([])
            elif i == 2:
                st1 = int(nextData(' ')[1:])
                st2 = int(nextData(' ')[1:])
                RD = nextData(',')
                WR = nextData(',')
                DIR = nextData('')
                TFE[st1].append(Transition(st2, RD, WR, DIR))
            elif i == 3: alphabet.append(reader)
            reader = read()

# Simulação da Máquina de Turing
def simulate(iter):
    global string
    stt = q = 0
    while iter > 0:
        print "> "+string[:stt]+"[q"+str(q)+"]"+string[stt:]
        for j in range(0, len(TFE[q])+1):
            if j == len(TFE[q])+1:
                quit()
            if TFE[q][j].RD == string[stt]:
                break
        Trans = TFE[q][j]
        string = string[0:stt]+Trans.WR+string[stt+1:]
        q = Trans.st
        stt = stt + Trans.DIR
        if stt == len(string):
            string = string + "B"
        iter = iter - 1

# Dados da Máquina de Turing
alphabet = []   # Alfabeto de entradas.
TFE = []        # Tabela  de Fluxo de Estados.
string = ""     # Cadeia a ser simulada.

# Rotina main()
print "*************************************"
print "*                                   *"
print "*   Simulador da Máquina de Turing  *"
print "*                                   *"
print "*************************************"
arquivo = open('MT.txt', 'r')
readMT()
string = alphabet.pop()
result = simulate(5)
