import sys
from grafo import Grafo
from copy import deepcopy

# Edmonds-Karp (Exercício 1)
# ----------------------------------------------------------------------------------------------------------------------
def maxFlow(grafo):
  if not grafo.s:
    raise Exception('Por favor, utilize um grafo dirigido')

  # Busca em Largura (Edmonds-Karp)
  def BFS(grafo, f):
    # Configurando variáveis
    s = grafo.fonte
    t = grafo.destino
    C = dict.fromkeys(grafo.V.keys(), False)
    A = dict.fromkeys(grafo.V.keys())

    # Inicializando
    C[s] = True
    Q = [s] # Fila de vértices

    while Q:
      u = Q.pop()

      for v in grafo.vizinhos(u):
        if not C[v] and grafo.peso(u, v) > f[(u, v)]:
          C[v] = True
          A[v] = u

          # Destino encontrado
          if v == t:
            p = [t]
            w = t

            while w != s:
              w = A[w]
              if w not in p:
                p.insert(0, w)

            return [tuple(p[i-1:i+1]) for i in range(1, len(p))]
          
          Q.append(v)
    
    return None
    # end BFS
  
  # Configurando todos os vértices
  f = dict.fromkeys(grafo.E.keys(), 0)

  while True:
    # Enquanto existir um caminho aumentante p na rede residual de s a t
    p = BFS(grafo, f)
    if not p:
      break
    
    # Atualiza o fluxo
    c = min([(grafo.peso(u, v) - f[(u, v)]) for u, v in p])
  
    for u, v in p:
      f[(u, v)] += c

  # Imprime o fluxo máximo
  print(sum([f[x] for x in grafo.arestas(grafo.fonte)]))

# Hopcroft-Karp (Exercício 2)
# ----------------------------------------------------------------------------------------------------------------------
def maxMatching(grafo):
  if grafo.s:
    raise Exception('Por favor, utilize um grafo nao dirigido')

  # Busca em largura
  def BFS():
    # Fila
    Q = []

    for x in X:
      if not mate[x]:
        D[x] = 0
        Q.append(x)
      else:
        D[x] = sys.float_info.max
    
    D[None] = sys.float_info.max

    while Q:
      x = Q.pop()

      if D[x] < D[None]:
        for y in grafo.vizinhos(x):
          if D[mate[y]] == sys.float_info.max:
            D[mate[y]] = D[x] + 1
            Q.append(mate[y])
    
    return D[None] != sys.float_info.max
    # end BFS

  # Busca em profundidade
  def DFS(x):
    if x:
      for y in grafo.vizinhos(x):
        if D[mate[y]] == D[x] + 1:
          if DFS(mate[y]):
            mate[y] = x
            mate[x] = y

            return True
    
      D[x] = sys.float_info.max

      return False
    
    return True
    # end DFS

  # Configurando variáveis
  V = list(grafo.V.keys())                          # Vértices X + Y
  X = V[:len(V)//2]                                 # Vértices X
  D = dict.fromkeys(V + [None], sys.float_info.max) # Distâncias
  mate = dict.fromkeys(V)                           # Emparelhamento
  m = 0                                             # Tamanho do emparelhamento

  while BFS():
    for x in X:
      if not mate[x]:
        if DFS(x):
          m += 1

  # Imprime o valor do emparelhamento máximo e quais arestas pertencem a ele
  print(m)
  print(*list(mate.items())[:len(V)//2], sep=', ')

# Coloração de vértices (Exercício 3)
# ----------------------------------------------------------------------------------------------------------------------
def greedyColoring(grafo):
  if grafo.s:
    raise Exception('Por favor, utilize um grafo nao dirigido')

  # Configurando variáveis
  colors = dict.fromkeys(grafo.V.keys())
  noColor = deepcopy(grafo)
  k = 0

  # Enquanto existirem vértices sem cor
  while noColor.qtdVertices():
    avG = deepcopy(noColor)

    # Enquanto houverem vértices que podem ser coloridos
    while avG.qtdVertices():
      # Escolhe o vértice com maior número de arestas
      vertex = max([(avG.grau(v), v) for v in avG.V.keys()])[1]
      colors[vertex] = k
      noColor.removeVertices([vertex])
      
      avG.removeVertices(avG.vizinhos(vertex) + [vertex])

    k += 1

  # Imprime a coloração mínima e as cores de cada vértice
  print(max(colors.values()) + 1)
  print(colors)