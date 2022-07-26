# Sistema de Manipulação de Grafos

Sistema manipulador de grafos dirigidos e não dirigidos, desenvolvido em Python.

O sistema é capaz de executar diversas operações em grafos:
- Busca em largura;
- Verificação de ciclos Eulerianos;
- Menor caminho através do algoritmo de Dijkstra;
- Aplicação do algoritmo de Floyd-Warshall;
- Componentes fortemente conexos; 
- Ordenação topológica;
- Árvore geradora mínima;
- Algoritmo de fluxo máximo, através de Edmonds-Karp;
- Emparelhamento máximo, através de Hopcroft-Karp;
- Coloração de vértices;

## Arquivo de Entrada

O arquivo de entrada segue o formato abaixo. 
Na primeira linha, n é o número de vértices. 
Nas linhas seguintes e antes da palavra “*edges”, há uma listagem de rótulos dos vértices. 
Note que cada vértice possui um ı́ndice de 1 à n.
Esse ı́ndice é importante, pois ele é utilizado nas definições das arestas. 
Depois da palavra “*edges” cada linha conterá uma aresta. 

Por exemplo, na linha onde há “a b valor do peso”, a e b são os vértices que a aresta conecta, valor do peso é o peso da aresta.

Para o caso de grafos dirigidos, a palavra "*arcs" aparece no lugar de "*edges".
```
*vertices n
1 rotulo_de_1
2 rotulo_de_2
...
n label_de_n
*edges
a b valor_do_peso
a c valor_do_peso
...
```

## Execução

Para executar um programa teste, utilize:
```
python3 main.py
```