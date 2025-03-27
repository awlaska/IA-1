import csv


def importar_grafo_csv(nome_ficheiro):
    # Dicionário para mapear nós a índices
    mapa_nos = {}

    # Lista para armazenar arestas lidas do CSV
    arestas = []

    # Ler o ficheiro CSV e armazenar as arestas
    with open(nome_ficheiro, newline='', encoding='utf-8') as ficheiro:
        leitor = csv.reader(ficheiro)
        next(leitor)

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
    matriz_adjacencia = [[None for _ in range(tamanho)] for _ in range(tamanho)]  # Inicializa com infinito

    # Preencher matriz com os valores das arestas
    for origem, destino, distancia in arestas:
        i, j = mapa_nos[origem], mapa_nos[destino]
        matriz_adjacencia[i][j] = distancia

    return matriz_adjacencia, mapa_nos

matriz_adjacencia, mapa_nos = importar_grafo_csv('graph.csv')

# Exibir a matriz de adjacência
for linha in matriz_adjacencia:
    print(linha)

# Exibir o mapeamento de cidades para índices
print(mapa_nos)