# -*- coding: cp1252 -*-
#
#       Simulador de 2AFD      
#   
#  Autores: Felipe Tuyama & Luciano Holanda     
import sys

def wash(saida):
    saida = saida.replace('\t','')
    saida = saida.replace(' ','')
    return saida

def read():
    return arquivo.readline().rstrip()
    
# Leitura da especificação do 2AFD
def nextData():
    global reader
    begin = 1
    while begin < len(reader) and reader[begin] != '\t': 
        begin += 1
    info = reader[1:begin]
    reader = reader[begin:len(reader)]
    return info
            
# Leitura do Arquivo de Entrada
def read2AFD():
    global reader
    for i in range(0, 6):
        reader = ""
        while reader != "#":
            reader = read()
        reader = read()
        while reader != "#":
            if i == 0:   alphabet.append(wash(reader))
            elif i == 1: states.append(wash(reader))
            elif i == 2: accept.append(wash(reader))
            elif i == 3:
                TFE.append([])
                for a in range(0, len(alphabet)):
                    TFE[len(TFE)-1].append(nextData())
            elif i == 4:
                Tdir.append([])
                TPT.append([])
                for a in range(0, len(alphabet)):
                    Tdir[len(Tdir)-1].append(nextData())
                    TPT[len(TPT)-1].append(0)
            elif i == 5:
                alphabet.append(wash(reader))
            reader = read()
 
# Simulação da 2AFD
def simulate():
    q = stt = 0
    while stt < len(u):
        print "> "+u[0:stt]+"("+states[q]+")"+u[stt:len(u)]
        alpha = alphabet.index(u[stt])
        if   (Tdir[q][alpha]=="R"): stt += 1
        elif (Tdir[q][alpha]=="L"): stt -= 1
        q = states.index(TFE[q][alpha])
        if(TPT[q][alpha] == stt):
            print "\n> "+u[0:stt]+"("+states[q]+")"+u[stt:len(u)]
            print "\nLoop Infinito!\n"
            return False
        TPT[q][alpha] = stt
        sys.stdin.read(1)
    print "> "+u[0:stt]+"("+states[q]+")"+u[stt:len(u)]
    return (states[q] in accept)

u = ""
# Dados do nosso 2AFD
alphabet = []   # Alfabeto de entradas
states = []     # Estados do 2AFD
accept = []     # Estados de aceitação
TFE = []        # (Tabela de Fluxo de Estados)
TPT = []        # (Tabela de posição de transição) - Indentificar Loop infinito
Tdir = []       # (Tabela de direções)

# Rotina main()
print "**************************"
print "*   Simulador de 2AFD    *"
print "**************************"
arquivo = open('2AFD.txt', 'r')
read2AFD()
u = alphabet.pop()
result = simulate()
if result:  print "[Cadeia Aceita]"
else:       print "[Cadeia Rejeitada]"
print "**************************"
