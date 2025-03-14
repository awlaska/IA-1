import random
import math
import sys
import os 

from cvs_to_matrix_3 import importar_grafo_csv_3


def rrt_connect(matriz_adjacencia, mapa_nos, inicio, fim, max_iter=1000):
    """
    Algoritmo RRT-Connect que usa a matriz de adjacência.
    :param matriz_adjacencia: Matriz de adjacência do grafo.
    :param mapa_nos: Dicionário que mapeia nodos para índices.
    :param inicio: Nodo de início (string).
    :param fim: Nodo de destino (string).
    :param max_iter: Número máximo de iterações.
    :return: Caminho encontrado.
    """
    def get_neighbors(nodo):
        # Retorna os vizinhos de um nodo
        return [vizinho for vizinho, custo in enumerate(matriz_adjacencia[nodo]) if custo is not None]

    def distancia(nodo1, nodo2):
        # Distância Euclidiana entre dois nodos
        return math.sqrt((nodo2[0] - nodo1[0]) ** 2 + (nodo2[1] - nodo1[1]) ** 2)

    inicio_idx = mapa_nos[inicio]
    fim_idx = mapa_nos[fim]

    arvore_inicio = {inicio_idx: None}
    arvore_fim = {fim_idx: None}

    for _ in range(max_iter):
        # Gera um nodo aleatório
        nodo_aleatorio = random.choice(list(mapa_nos.values()))

        # Expande a árvore a partir do início
        nodo_proximo_inicio = min(arvore_inicio.keys(), key=lambda x: distancia((x, 0), (nodo_aleatorio, 0)))
        for vizinho in get_neighbors(nodo_proximo_inicio):
            if vizinho not in arvore_inicio:
                arvore_inicio[vizinho] = nodo_proximo_inicio

        # Expande a árvore a partir do fim
        nodo_proximo_fim = min(arvore_fim.keys(), key=lambda x: distancia((x, 0), (nodo_aleatorio, 0)))
        for vizinho in get_neighbors(nodo_proximo_fim):
            if vizinho not in arvore_fim:
                arvore_fim[vizinho] = nodo_proximo_fim

        # Verifica se as árvores se conectaram
        intersecao = set(arvore_inicio.keys()).intersection(set(arvore_fim.keys()))
        if intersecao:
            nodo_conexao = intersecao.pop()
            caminho_inicio = []
            current = nodo_conexao
            while current is not None:
                caminho_inicio.append(current)
                current = arvore_inicio[current]
            caminho_inicio.reverse()

            caminho_fim = []
            current = nodo_conexao
            while current is not None:
                caminho_fim.append(current)
                current = arvore_fim[current]

            caminho_total = caminho_inicio + caminho_fim[1:]
            caminho_total_nomes = [list(mapa_nos.keys())[idx] for idx in caminho_total]
            return caminho_total_nomes

    return None  # Se não encontrar caminho

# Exemplo de uso
matriz, mapa = importar_grafo_csv_3("graph3_2.csv")
caminho = rrt_connect(matriz, mapa, "A", "T")
print("Caminho encontrado:", caminho)