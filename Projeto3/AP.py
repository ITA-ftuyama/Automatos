# -*- coding: cp1252 -*-
#
#       Simulador de Autômato de Pilha    
#   
#  Autores: Felipe Tuyama     
import copy

# Implementação da Fila
class Fila(object):
    def __init__(self):
        self.dados = []
    def insere(self, elemento):
        self.dados.append(elemento)
    def remove(self):
        return self.dados.pop(0)
    def vazia(self):
        return len(self.dados) == 0
    def length(self):
        return len(self.dados)

# Implementação da Pilha
class Pilha(object):
    def __init__(self):
        self.dados = []
    def insere(self, elemento):
        if elemento != "":
            self.dados.append(elemento)
    def remove(self):
        if not self.vazia():
            return self.dados.pop(-1)
    def vazia(self):
        return len(self.dados) == 0
    def length(self):
        return len(self.dados)
    def inTopo(self, elemento):
        if elemento == "":
            return True
        return elemento == self.topo()
    def topo(self):
        if not self.vazia():
            return self.dados[len(self.dados)-1]
    def log(self):
        info = "Pilha: "
        for i in range(0, len(self.dados)):
            info += self.dados[i]
        return info

# Nó de Transição
class Transition(object):
    def __init__(self, st2, sym, rem, add):
        self.st = st2
        self.sym = sym
        self.add = add
        self.rem = rem
        
# Status da Busca BFS (elementos da Fila):
class CheckPoint(object):
    def __init__(self, q, stt, P):
        self.q = q
        self.stt = stt
        self.P = P

# Remove Tabs e Espaços da linha lida         
def wash(saida):
    saida = saida.strip('\t')
    saida = saida.strip('\b')
    return saida
    
# Leitura da Transição do AP
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

# Leitura do Arquivo de Entrada
def readAP():
    global reader
    for i in range(0, 6):
        reader = " "
        while reader[0] != '#':
            reader = read()
        reader = read()
        while reader[0] != '#':
            if i == 0:   alphabet.append(wash(reader))
            elif i == 1: states.append(wash(reader))
            elif i == 2:
                initial.append(wash(reader))
                for j in range(0, len(states)):
                    TFE.append([])
            elif i == 3: accept.append(wash(reader))
            elif i == 4:
                st1 = nextData(' ')
                st2 = nextData(' ')
                sym = nextData(',')
                rem = nextData('/')
                add = nextData('')
                Trans = Transition(st2, sym, rem, add)
                TFE[states.index(st1)].append(Trans)
            elif i == 5: alphabet.append(wash(reader))
            reader = read()

# Simulação do Autômato de Pilha
def simulate():
    global P, F
    stt = q = 0
    No = CheckPoint(states.index(initial[0]),0,P)
    F.insere(No)
    while not F.vazia():
        No = F.remove()
        P = No.P
        q = No.q
        stt = No.stt
        print "> "+string[:stt]+"["+states[q]+"]"+string[stt:]+"  "+P.log()
        if No.stt >= len(string):
            if states[No.q] in accept:
                if P.vazia():
                    return True
        for j in range(0, len(TFE[No.q])):
            Trans = TFE[No.q][j]
            if (No.stt<len(string) and Trans.sym == string[No.stt]) or Trans.sym == "":
                if No.P.inTopo(Trans.rem):
                    q = states.index(Trans.st)
                    P.insere(Trans.add)
                    if Trans.rem != "":
                        P.remove()
                    if Trans.sym != "":
                        stt += 1
                    Noq = CheckPoint(q, stt, copy.deepcopy(P))
                    F.insere(Noq)
    return False

# Dados do Autômato de Pilha
alphabet = []   # Alfabeto de entradas.
states = []     # Estados  do AP.
initial = []    # Estado inicial
accept = []     # Estados  de aceitação.
TFE = []        # Tabela  de Fluxo de Estados.
string = ""     # Cadeia a ser simulada.
P = Pilha()     # Pilha do Autômato de Pilha
F = Fila()      # Fila para a simulação BFS

# Rotina main()
print "*************************************"
print "*                                   *"
print "*   Simulador de Autômato de Pilha  *"
print "*                                   *"
print "*************************************"
arquivo = open('APa.txt', 'r')
readAP()
string = alphabet.pop()
result = simulate()
if result:  print "[Cadeia Aceita]"
else:       print "[Cadeia Rejeitada]"
print "**************************"
