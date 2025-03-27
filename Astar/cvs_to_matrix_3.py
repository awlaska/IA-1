import csv

def importar_grafo_csv_3(nome_ficheiro):
    # Dicionário para mapear nós a índices
    mapa_nos = {}

    # Lista para armazenar arestas lidas do CSV
    arestas = []

    # Ler o ficheiro CSV e armazenar as arestas
    with open(nome_ficheiro, newline='', encoding='utf-8') as ficheiro:
        leitor = csv.reader(ficheiro)
        next(leitor)  # Pula a primeira linha (cabeçalho)
        
        for linha in leitor:
            origin_city, destination_city, toll, fuel, distance_km = linha[0], linha[1], float(linha[2]), float(linha[3]), float(linha[4])
            arestas.append((origin_city, destination_city, toll, fuel, distance_km))

            # Adicionar nós ao dicionário se ainda não estiverem mapeados
            if origin_city not in mapa_nos:
                mapa_nos[origin_city] = len(mapa_nos)
            if destination_city not in mapa_nos:
                mapa_nos[destination_city] = len(mapa_nos)

    # Criar matriz de adjacência
    tamanho = len(mapa_nos)
    matriz_adjacencia = [[None for _ in range(tamanho)] for _ in range(tamanho)]  # Inicializa com None

    # Preencher matriz com os valores das arestas
    for origin_city, destination_city, toll, fuel, distance_km in arestas:
        i, j = mapa_nos[origin_city], mapa_nos[destination_city]
        matriz_adjacencia[i][j] = {'toll': toll, 'fuel': fuel, 'distance_km': distance_km}

    return matriz_adjacencia, mapa_nos

matriz_adjacencia, mapa_nos = importar_grafo_csv_3('../cidades.csv')

# Exibir a matriz de adjacência
for linha in matriz_adjacencia:
    print(linha)

# Exibir o mapeamento de cidades para índices
print(mapa_nos)