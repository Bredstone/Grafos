import sys, itertools
from grafo import Grafo
from copy import deepcopy

# Função auxiliadora para impressão dos dados
# ---------------------------------------------------------------------------------------------------------------------
def formatNumber(n):
  if n == sys.float_info.max: return 'infinito'
  return n if n%1 else int(n)

# Função de busca em largura
# ---------------------------------------------------------------------------------------------------------------------
def buscaBFS(arquivo, s):
  # Lê o arquivo e retorna um grafo
  grafo = Grafo.ler(arquivo)

  # Verifica se o vértice é válido
  if s not in grafo.V:
    raise Exception('Vertice invalido')
  
  # Define o array de visitados e de tempos
  c = dict.fromkeys(grafo.V.keys(), False)
  t = dict.fromkeys(grafo.V.keys(), -1)
  
  # Tempo do vértice inicial = 0 e vértice incial já visitado
  c[s] = True
  t[s] = 0

  # Fila de vértices a serem iterados
  fila = [s]

  # Enquanto a fila não estiver vazia:
  while fila:
    u = fila.pop(0)
    for v in [v for v in grafo.vizinhos(u) if not c[v]]:
        c[v] = True
        t[v] = t[u] + 1
        fila.append(v)

  # Manuseio de dados para impressão dos resultados
  for i in range(max(t.values()) + 1):
    print('{}: '.format(i), end='')
    print(*[a for a, b in t.items() if t[a] == i], sep=', ')

# Função que encontra um ciclo euleriano
# ---------------------------------------------------------------------------------------------------------------------
def cicloEuler(grafo):
  # Define o array de visitados
  c = dict.fromkeys(grafo.E.keys(), False)

  # Define o caminho atual, iniciando pelo primeiro vértice
  caminhoAtual = [list(grafo.V.keys())[0]]

  # Array de resultados
  ciclo = []

  while True:
    # Vértice atual = último vértice do caminho atual
    verticeAtual = caminhoAtual[-1]

    # Se existirem arestas não visitadas, vizinhas ao vértice atual:
    arestasNV = [e for e in grafo.arestas(verticeAtual) if not c[e]]
    if arestasNV:
      arestaProx = arestasNV[0]
      c[arestaProx] = True

      verticeProx = list(arestaProx)
      verticeProx.remove(verticeAtual)

      caminhoAtual.append(verticeProx[0])
    else:
      break
  
  # Monta o array de resultado
  while caminhoAtual:
    ciclo.append(caminhoAtual.pop())
  
  # Se encontrou um ciclo:
  if all(c.values()) and ciclo[0] == ciclo[-1]:
    print(1)
    ciclo.reverse()
    print(*ciclo, sep=', ')
  # Caso contrário:
  else:
    print(0)

# Função de Dijkstra para menor caminho
# ---------------------------------------------------------------------------------------------------------------------
def dijkstra(arquivo, s):
  # Lê o arquivo e retorna um grafo
  grafo = Grafo.ler(arquivo)

  # Verifica se o grafo não possui pesos negativos
  if not all([x >= 0 for x in grafo.E.values()]):
    raise Exception('Grafo com pesos negativos')

  # Verifica se o vértice é válido
  if s not in grafo.V:
    raise Exception('Vertice invalido')
  
  # Arrays de distância, antecessores e visitados
  d = dict.fromkeys(grafo.V.keys(), sys.float_info.max)
  a = dict.fromkeys(grafo.V.keys(), [])
  c = dict.fromkeys(grafo.V.keys(), False)
  
  # Distância do vértice inicial = 0 e antecessor ao vértice inicial = vértice inicial
  d[s] = 0
  a[s] = [s]

  # Enquanto não forem visitados todos os vértices:
  while not all(c.values()):
    # Seleciona, entre os não visitados, o vértice com menor distância e o marca como visitado
    x = [k for k, v in d.items() if v == min([d[x] for x in c.keys() if not c[x]]) and not c[k]][0] 
    c[x] = True
    
    # Itera sobre as arestas do vértice atual
    for u, v in grafo.arestas(x):
      if d[v] > d[u] + grafo.peso(u, v):
        d[v] = d[u] + grafo.peso(u, v)
        a[v] = a[u] + [v]
      if d[u] > d[v] + grafo.peso(u, v):
        d[u] = d[v] + grafo.peso(u, v)
        a[u] = a[v] + [u]

  # Manuseio de dados para impressão dos resultados
  for i in grafo.V.keys():
    print('{}: '.format(i), end='')
    print(*a[i], sep=', ', end='')
    print('; d={}'.format(formatNumber(d[i])))

# Função de Floyd-Warshall
# ---------------------------------------------------------------------------------------------------------------------
def warshall(arquivo):
  # Lê o arquivo e retorna um grafo
  grafo = Grafo.ler(arquivo)

  # Dicionário que simula a matriz de adjacência
  p = dict.fromkeys(list(itertools.combinations_with_replacement(grafo.V.keys(), 2)), sys.float_info.max)
  p = {**p, **dict.fromkeys([(x, x) for x in grafo.V.keys()], 0), **grafo.E}
  
  # Atualiza a distância |V| vezes
  for k in grafo.V.keys():
    for u, v in itertools.combinations_with_replacement(grafo.V.keys(), 2):
      b = tuple(sorted([k, u]))
      c = tuple(sorted([k, v]))

      p[(u, v)] = min(p[(u, v)], p[b] + p[c])

  # Manuseio de dados para impressão dos resultados
  for a in grafo.V.keys():
    print('{}:'.format(a), end=' ')
    print(*[formatNumber(p[(tuple(sorted([a, b])))]) for b in grafo.V.keys()], sep=', ')

# Componentes Fortemente Conexos
# ----------------------------------------------------------------------------------------------------------------------
def componentesFC(grafo):
  # Verifição do grafo indicado
  if not grafo.s:
    raise Exception('Por favor, utilize grafos dirigidos!')

  # Algoritmo 16 - modificado
  # Se signal = True, imprime os resultados
  def DFS(grafo, keys = grafo.V.keys(), signal = False):
    # Algoritmo 17 - simplificado
    def DFSvisit(v):
      visitados[v] = True

      for u in grafo.vizinhos(v):
        if not visitados[u]: DFSvisit(u)

      stack.insert(0, v)
      # end DFSvisit

    # Inicializando as variáveis
    stack = []
    visitados = dict.fromkeys(keys, False)

    for v in keys:
      if not visitados[v]:
        DFSvisit(v)
        # Impressão dos resultados
        if signal:
          print(*sorted(stack), sep=', ')
          stack = []
    
    return stack
    # end DFS

  stack = DFS(grafo)        # Computa DFS do grafo
  g = grafo.transpose()     # Inverte os arcos do grafo
  DFS(g, stack, True)       # Imprime os resultados

# Ordenação Topológica
# ----------------------------------------------------------------------------------------------------------------------
def ordenacao(grafo):
  # Verifição do grafo indicado
  if not grafo.s:
    raise Exception('Por favor, utilize grafos dirigidos!')

  # Algoritmo 19 - simplificado
  def DFSord(v):
    visitados[v] = True

    for u in grafo.vizinhos(v)[::-1]:
      if not visitados[u]:
        DFSord(u)
    
    order.insert(0, v)
    # end DFSord

  # Inicializando as variáveis
  visitados = dict.fromkeys(grafo.V.keys(), False)
  order = []

  for u in grafo.V.keys():
    if not visitados[u]:
      DFSord(u)
  
  # Impressão dos resultados
  result = ' -> '.join([grafo.rotulo(v) for v in order]).replace('"', '')
  print(result)

# Árvore Geradora Mínima
# Kruskal
# ----------------------------------------------------------------------------------------------------------------------
def arvoreMinima(grafo):
  # Verifição do grafo indicado
  if grafo.s:
    raise Exception('Por favor, utilize grafos nao dirigidos!')
  
  # Inicializando as variáveis
  A = []
  S = {}
  for x in grafo.V.keys(): S[x] = [x]
  E = [x[0] for x in sorted(grafo.E.items(), key=lambda item: item[1])]
  sumR = 0

  for (u, v) in E:
    if S[u] != S[v]:
      A += [(u, v)]
      sumR += grafo.E[(u, v)]
      x = S[u] + S[v]

      for y in x:
        S[y] = x

  # Impressão dos resultados
  print(sumR if sumR%1 else int(sumR))
  print(*[str(u) + '-' + str(v) for (u, v) in A], sep=', ')

# Edmonds-Karp
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

# Hopcroft-Karp
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

# Coloração de vértices
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