#
#      Analisador sintático bottom-up de GLC na FNG
#
#  Autores: André Simão
#           Felipe Tuyama
#           Matheus Leão
#           Marco Aurélio
import sys

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

    def first(self):
        return self.dados[0]

    def log(self):
        print "Imprimindo a fila:"
        for i in range(0, len(self.dados)):
            self.dados[i].log()

# Armazena a arvore de derivaçoes para imprimir a derivação que produz
# a cadeia fornecida na entrada


class Noh(object):

    def __init__(self, w, father):
        self.w = w
        self.father = father

    def log(self):
        # print "self.w = " + str(self.w)
        if self.father:
            print str("father[ " + str(self.w) + " ] = " + str(self.father.w))
        else:
            print str("father[ " + str(self.w) + " ] = " + "None")

# Leitura da Gramática na FNG:


def readGrammar():
    global reader
    global V
    global Sig
    global S
    grammarFile = open('GLC.txt', 'r')
    # Cada linha do arquivo é posta em uma lista:
    reader = grammarFile.readlines()

    # Construindo V
    V = str(reader[0]).split(' ')
    V[-1] = V[-1].strip()

    # Construindo Sig
    Sig = str(reader[1]).split(' ')
    Sig[-1] = Sig[-1].strip()

    # Construindo S
    S = reader[2]
    S = S.strip()

    # Construindo P
    for i in range(3, len(reader)):
        prod = str(reader[i]).split(' ')
        prod[-1] = prod[-1].strip()
        if(len(prod) == 1):
            prod = prod + [""]
        if not prod[0] in P:
            P[prod[0]] = [prod[1]]
        else:
            P[prod[0]] = P[prod[0]] + [prod[1]]

    # Construindo Pinv
    for i in range(3, len(reader)):
        prod = str(reader[i]).split(' ')
        prod[-1] = prod[-1].strip()
        if len(prod) == 1:
            prod = prod + [""]
        if not prod[1] in Pinv:
            Pinv[prod[1]] = [prod[0]]
        else:
            Pinv[prod[1]] = Pinv[prod[1]] + [prod[0]]

    # Adicionando as produções indiretas obtidas através das produção vazia
    if "" in Pinv:
        for i in range(3, len(reader)):
            prod = str(reader[i]).split(' ')
            prod[-1] = prod[-1].strip()
            if len(prod) == 2:
                s = prod[1]
                nDeriv = 0
                for j in range(0, len(prod[1])):
                    if s[j-nDeriv] in Pinv[""]:
                        lastS = s
                        s = s[:j-nDeriv] + s[j+1-nDeriv:]
                        if not s in Pinv:
                            Pinv[s] = [lastS]
                        else:
                            Pinv[s] = Pinv[s] + [lastS]
                        nDeriv += 1

    grammarFile.close()


def testReadGrammar():
    print "V:"
    print V
    print "Sig:"
    print Sig
    print "S:"
    print S
    print "P:"
    print P
    print "Pinv:"
    print Pinv
    print "PIndDeriv:"
    print PIndDeriv
    print "PInvIndDeriv:"
    print PInvIndDeriv

# Leitura da Cadeia a ser analisada:


def readCadeia():
    global reader
    stringFile = open('string.txt', 'r')
    # Generalizar para várias cadeias?
    string = stringFile.readline()
    stringFile.close()
    return string

# Verifica se existe uma redução válida


def addReduction(w, father):
    F.insere(Noh(w, father))


def stringReduction(n):
    w = n.w
    newReduction = ""
    Pointer = len(w) - 1
    if Pointer < 0:  # Caso w seja a cadeia vazia ("")
        return

    Pointer = len(w) - 1
    while not w[Pointer] in Sig:
        Pointer -= 1
        if Pointer < 0:
            return

    # Para cada regra de Produção:
    for j in range(Pointer+1, len(w) + 1):
        # Procuro uma derivação direta que produza parte de w:
        if w[Pointer:j] in Pinv:
            # Expando o nó, colocando os filhos na Fila:
            # Esse novo for (em k) é para considerar dois simbolos distintos
            # produzindo a mesma coisa
            # Ex.: A -> aB && B -> aB
            for k in range(0, len(Pinv[w[Pointer:j]])):
                addReduction(w[:Pointer] + Pinv[w[Pointer:j]][k] + w[j:], n)

# Parser bottom-up da cadeia w:


def BFSparser():
    F.insere(Noh(string, None))
    # F.log()
    while not F.vazia():
        #F.log()
        if (F.first().w == S):
            return F.first()
        # print F.dados
        stringReduction(F.first())
        F.remove()
    return None

# Imprime a sequencia de derivações para se chegar na cadeia fornecida


def printPath(n):
    s = ""
    while n.father != None:
        s += n.w
        s += " "
        n = n.father
    s += n.w
    print s


# Dados da nossa gramática (Rascunho, pode mudar):
V = []      # Lista de Símbolos não Terminais
Sig = []    # Lista de Símbolos Terminais
S = ""      # Símbolo inicial S pertencente a V

P = {}    # Matriz de Produções:
# Agora P é um dicionário
# P["S"] é a lista de produções do Símbolo não Terminal S (número 0)
# P["A"] é a lista de produções do Símbolo não Terminal A (número 1)
# ...  (assim por diante)

# Por exemplo:
# Se S-> a  &&  S-> aB && A-> b
# Teríamos
# P["S"] = [ "a" , "aB" ]
# P["A"] = [ "b" ]
# P =   {
#           "S": [ "a" , "aB" ],
#           "A": [ "b" ]
#       }

Pinv = {}  # Semelhante à matriz de Produções P, só que na ordem inversa:
# Agora as keys são a parte direita de cada produção e os values
# são a parte esquerda da produção
# Por exemplo:
# Se S-> a  &&  S-> aB && A-> b
# Teríamos
# Pinv["a"] = "S"
# Pinv["aB"] = "S"
# Pinv["b"] = "A"
# Pinv =    {
#               "a": "S",
#               "aB": "S",
#               "A":
#           }
# Essa Pinv vai ser útil para o BFSparser
# As produções vazias estão em Pinv = {"": ["A", "B"], ...}
# Portanto Pinv[""] representa a lista de simbolos que produzem
# a cadeia vazia

F = Fila()  # Fila usada para o BFS

# Código principal - Rotina main()
# print "**************************"
# print "*   Parser bottom-up     *"
# print "**************************"
readGrammar()
#testReadGrammar()
string = readCadeia()      # Cadeia a ser analisada
if not string:         	# Caso especial, cadeia vazia
    if ("" in P[S]):
        print 1
        print S
    else:
        print 0

else:
    result = BFSparser()
    if result:
        print 1
        #print "[Cadeia pertence a linguagem da Gramatica]"
        printPath(result)
        # Informar a derivação
else:
    print 0
    #print "[Cadeia nao pertence a linguagem da Gramatica]"
# print "**************************"
