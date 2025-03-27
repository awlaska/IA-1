#TODO pensa infinitamente
import csv
import heapq


def importar_grafo_csv_3(nome_ficheiro):
    mapa_nos = {}
    arestas = []

    with open(nome_ficheiro, newline='', encoding='utf-8') as ficheiro:
        leitor = csv.reader(ficheiro)
        next(leitor)

        for linha in leitor:
            origin_city, destination_city, toll, fuel, distance_km = linha[0], linha[1], float(linha[2]), float(
                linha[3]), float(linha[4])
            arestas.append((origin_city, destination_city, toll, fuel, distance_km))

            if origin_city not in mapa_nos:
                mapa_nos[origin_city] = len(mapa_nos)
            if destination_city not in mapa_nos:
                mapa_nos[destination_city] = len(mapa_nos)

    tamanho = len(mapa_nos)
    matriz_adjacencia = [[None for _ in range(tamanho)] for _ in range(tamanho)]

    for origin_city, destination_city, toll, fuel, distance_km in arestas:
        i, j = mapa_nos[origin_city], mapa_nos[destination_city]
        matriz_adjacencia[i][j] = {'toll': toll, 'fuel': fuel, 'distance_km': distance_km}

    return matriz_adjacencia, mapa_nos


def a_star_todos_caminhos(matriz_adjacencia, mapa_nos, inicio, fim):
    if inicio not in mapa_nos or fim not in mapa_nos:
        raise ValueError("Cidade de início ou fim não encontrada no mapa.")

    inicio_idx = mapa_nos[inicio]
    fim_idx = mapa_nos[fim]
    fila = [(0, 0, inicio_idx, [inicio_idx])]
    caminhos = []

    while fila:
        custo_estimado, custo_atual, no_atual, caminho = heapq.heappop(fila)

        if no_atual == fim_idx:
            caminhos.append((caminho, custo_atual))
            continue

        for vizinho, dados in enumerate(matriz_adjacencia[no_atual]):
            if dados is not None:
                novo_custo = custo_atual + dados['toll'] + dados['fuel'] + dados['distance_km']
                heapq.heappush(fila, (novo_custo, novo_custo, vizinho, caminho + [vizinho]))

    return caminhos


def calcular_custos_individuais(matriz_adjacencia, mapa_nos, caminho):
    toll_total, fuel_total, distance_total = 0, 0, 0

    for i in range(len(caminho) - 1):
        origem_idx, destino_idx = caminho[i], caminho[i + 1]
        dados = matriz_adjacencia[origem_idx][destino_idx]
        toll_total += dados['toll']
        fuel_total += dados['fuel']
        distance_total += dados['distance_km']

    return toll_total, fuel_total, distance_total

nome_ficheiro = "../cidades.csv"
matriz, mapa_nos = importar_grafo_csv_3(nome_ficheiro)
cidades = sorted(mapa_nos.keys())

print("\nCidades disponíveis:")
for i, cidade in enumerate(cidades, 1):
    print(f"{i}. {cidade}")

while True:
    try:
        inicio_idx = int(input("\nDigite o número da cidade de início: ")) - 1
        fim_idx = int(input("Digite o número da cidade de destino: ")) - 1
        inicio = cidades[inicio_idx]
        fim = cidades[fim_idx]
        break
    except (ValueError, IndexError):
        print("Entrada inválida. Por favor, digite números correspondentes às cidades listadas.")

try:
    matriz_adjacencia, mapa_nos = importar_grafo_csv_3(nome_ficheiro)
except FileNotFoundError:
    print(f"Erro: O ficheiro '{nome_ficheiro}' não foi encontrado.")
    exit()

caminhos = a_star_todos_caminhos(matriz_adjacencia, mapa_nos, inicio, fim)

if caminhos:
    print(f"\nForam encontrados {len(caminhos)} caminhos:")
    for i, (caminho, custo_total) in enumerate(caminhos, 1):
        caminho_cidades = [list(mapa_nos.keys())[idx] for idx in caminho]
        toll_total, fuel_total, distance_total = calcular_custos_individuais(matriz_adjacencia, mapa_nos, caminho)
        print(f"\nCaminho {i}: {' -> '.join(caminho_cidades)}")
        print(f"Custo total: {custo_total}")
        print(f"Km Cost: {distance_total}")
        print(f"Toll Cost: {toll_total}")
        print(f"Fuel Cost: {fuel_total}")
else:
    print("\nNão foi possível encontrar um caminho.")