import csv
import numpy as np


def importar_grafo_csv(nome_ficheiro):
    # Dicionário para mapear nós a índices
    mapa_nos = {}

    # Lista para armazenar arestas lidas do CSV
    arestas = []

    # Ler o ficheiro CSV e armazenar as arestas
    with open(nome_ficheiro, newline='', encoding='utf-8') as ficheiro:
        leitor = csv.reader(ficheiro)
        for linha in leitor:
            origem, destino, distancia = linha[0], linha[1], int(linha[2])
            arestas.append((origem, destino, distancia))

            # Adicionar nós ao dicionário se ainda não estiverem mapeados
            if origem not in mapa_nos:
                mapa_nos[origem] = len(mapa_nos)
            if destino not in mapa_nos:
                mapa_nos[destino] = len(mapa_nos)

    # Criar matriz de adjacência
    tamanho = len(mapa_nos)
    matriz_adjacencia = np.full((tamanho, tamanho), np.inf)  # Inicializa com infinito

    # Preencher matriz com os valores das arestas
    for origem, destino, distancia in arestas:
        i, j = mapa_nos[origem], mapa_nos[destino]
        matriz_adjacencia[i][j] = distancia

    return matriz_adjacencia, mapa_nos


# Exemplo de uso
matriz, mapa = importar_grafo_csv("grafo.csv")
print("Matriz de Adjacência:")
print(matriz)
print("Mapeamento dos nós:", mapa)
