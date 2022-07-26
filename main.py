import operacoes
from grafo import Grafo

print('Exercicio 1: ')
operacoes.maxFlow(Grafo.lerGR('tests/fluxo_maximo/wiki.gr'))

print('\nExercicio 2: ')
operacoes.maxMatching(Grafo.lerGR('tests/emparelhamento_maximo/pequeno.gr'))

print('\nExercicio 3: ')
operacoes.greedyColoring(Grafo.lerGR('tests/teste.gr'))