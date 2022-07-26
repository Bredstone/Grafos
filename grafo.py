import sys
import itertools

# Classe Grafo
class Grafo:
  # Método construtor (dicionário de vértices, array de caminhos, pesos)
  def __init__(self, V, E, w, s = True, fonte=None, destino=None):
    self.V = V

    # Verifica se o grafo é válido
    if not all([x in V for x in set(itertools.chain(*E))]):
      raise Exception('Grafo invalido')
    
    if s:
      self.E = dict(zip(E, w))
    else:
      self.E = dict(zip([tuple(sorted(x)) for x in E], w))
    self.s = s

    # Verifica se foi indicado uma fonte e um destino
    if not fonte:
      fonte = min(self.V)
    if not destino:
      destino = max(self.V)
    self.fonte = fonte
    self.destino = destino

  # Retorna a qtd de vértices
  def qtdVertices(self):
    return len(self.V)

  # Retorna a qtd de arestas
  def qtdArestas(self):
    return len(self.E)

  # Retorna uma lista de arestas de determinado vértice
  def arestas(self, v):
    if self.s:
      return list(filter(lambda x : v == x[0], self.E.keys()))
    else:
      return list(filter(lambda x : v in x, self.E.keys()))

  # Retorna o grau de determinado vértice
  def grau(self, v):
    return len(self.arestas(v))

  # Retorna o rótulo de determinado vértice
  def rotulo(self, v):
    try:
      return self.V[v]
    except:
      return ''

  # Retorna os vértices vizinhos de determinado vértice
  def vizinhos(self, v):
    return [x for x in list(itertools.chain(*self.arestas(v))) if x != v]

  # Verifica se há determinada aresta
  def haAresta(self, u, v):
    return any([v in x for x in self.arestas(u)])

  # Verifica o peso de determinada aresta
  def peso(self, u, v):
    if self.haAresta(u, v):
      return self.E[(u, v)]
    return sys.float_info.max

  # Retorna o grafo transposto
  def transpose(self):
    if self.s:
      return Grafo(self.V, [(v, u) for (u, v) in self.E.keys()], self.E.values(), self.s)
    else:
      return self

  # Remove vértices e arestas de um grafo
  def removeVertices(self, vertices):
    for v in vertices:
      if v in self.V.keys():
        self.V.pop(v)  
        for e in self.arestas(v):
          self.E.pop(e)

  # Lê um arquivo .net e retorna um grafo
  @staticmethod
  def ler(arquivo):
    try:
      rows = open(arquivo).readlines()
      rows = [row.split() for row in rows]

      # Vértices
      V = dict([(int(x), ' '.join(y)) for x, *y in rows[1 : int(rows[0][1]) + 1]])
      # Arestas ou arcos
      E = [(int(a), int(b)) for a, b, _ in rows[int(rows[0][1]) + 2 : ]]
      # Pesos
      w = [float(w) for _, _, w in rows[int(rows[0][1]) + 2 : ]]
      # Sinal
      s = True

      # Grafo não dirigido
      if rows[int(rows[0][1]) + 1][0] == "*edges":
        s = False
    except:
      raise Exception('Arquivo invalido')

    return Grafo(V, E, w, s)

  # Lê um arquivo .gr e retorna um grafo
  @staticmethod
  def lerGR(arquivo):
    try:
      rows = open(arquivo).readlines()
      V = []
      E = []
      w = []
      s = True
      fonte = None
      destino = None

      for row in rows:
        if row != '\n':
          row = row.split()

          # Vértices
          if row[0] == 'p':
            V = dict.fromkeys([i for i in range(1, int(row[2]) + 1)])
          
          # Fonte e destino
          if row[0] == 'n':
            if row[2] == 's':
              fonte = int(row[1])
            else:
              destino = int(row[1])

          # Arestas ou arcos
          if row[0] == 'a' or row[0] == 'e':
            E.append((int(row[1]), int(row[2])))
            try:
              w.append(float(row[3]))
            except:
              w.append(0)
          
          # Sinal
          if row[0] == 'e':
            s = False
    except:
      raise Exception('Arquivo invalido')

    return Grafo(V, E, w, s, fonte, destino)