import csv

def importar_grafo_csv_3(nome_ficheiro):
    # Dicionário para mapear nós a índices
    mapa_nos = {}

    # Lista para armazenar arestas lidas do CSV
    arestas = []

    # Ler o ficheiro CSV e armazenar as arestas
    with open(nome_ficheiro, newline='', encoding='utf-8') as ficheiro:
        leitor = csv.reader(ficheiro)
        for linha in leitor:
            origem, destino, kms, litros, minutos = linha[0], linha[1], int(linha[2]), int(linha[3]), int(linha[4])
            arestas.append((origem, destino, kms, litros, minutos))

            # Adicionar nós ao dicionário se ainda não estiverem mapeados
            if origem not in mapa_nos:
                mapa_nos[origem] = len(mapa_nos)
            if destino not in mapa_nos:
                mapa_nos[destino] = len(mapa_nos)

    # Criar matriz de adjacência
    tamanho = len(mapa_nos)
    matriz_adjacencia = [[None for _ in range(tamanho)] for _ in range(tamanho)]  # Inicializa com None

    # Preencher matriz com os valores das arestas
    for origem, destino, kms, litros, minutos in arestas:
        i, j = mapa_nos[origem], mapa_nos[destino]
        matriz_adjacencia[i][j] = {'kms': kms, 'litros': litros, 'minutos': minutos}

    return matriz_adjacencia, mapa_nos

# Exemplo de uso
print("Insira o nome do ficheiro: ")
nome_ficheiro = input()
matriz, mapa = importar_grafo_csv_3(nome_ficheiro + ".csv")
print("Matriz de Adjacência:")
for linha in matriz:
    print(linha)
print("Mapeamento dos nós:", mapa)