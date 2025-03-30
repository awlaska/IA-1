import csv
import heapq

def importar_grafo_csv(nome_ficheiro):
    mapa_nos = {}
    arestas = []

    with open("../" + nome_ficheiro, newline='', encoding='utf-8') as ficheiro:
        leitor = csv.reader(ficheiro)
        next(leitor)  # Ignora o cabeçalho

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

def importar_grafo_csv_3():
    choice = -1
    while choice != "0":
        choice = input("1. cidades.csv\n2. graph3.csv\n3. graph3_2.csv\n- ")
        if choice == "1":
            nome_ficheiro = "cidades.csv"
            matriz, mapa_nos = importar_grafo_csv(nome_ficheiro)

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
                    print("Entrada inválida. Por favor, escolha um número válido.")

            return nome_ficheiro, inicio, fim  # Retorna o nome do arquivo e as cidades corretamente

        elif choice == "2":
            return "graph3.csv", "A", "T"

        elif choice == "3":
            return "graph3_2.csv", "A", "K"

def a_star(matriz_adjacencia, mapa_nos, inicio, fim):
    # Verifica se as cidades de início e fim estão no mapa
    if inicio not in mapa_nos or fim not in mapa_nos:
        raise ValueError("Cidade de início ou fim não encontrada no mapa.")

    # Índices das cidades de início e fim
    inicio_idx = mapa_nos[inicio]
    fim_idx = mapa_nos[fim]

    # Fila de prioridade: (custo estimado, custo atual, nó atual, caminho)
    fila = [(0, 0, inicio_idx, [inicio_idx])]

    # Dicionário para armazenar os custos mínimos até cada nó
    custos_minimos = {inicio_idx: 0}

    while fila:
        # Pega o nó com o menor custo estimado
        custo_estimado, custo_atual, no_atual, caminho = heapq.heappop(fila)

        # Se chegamos ao destino, retorna o caminho e o custo
        if no_atual == fim_idx:
            caminho_cidades = [list(mapa_nos.keys())[idx] for idx in caminho]
            return caminho_cidades, custo_atual

        # Explora os vizinhos do nó atual
        for vizinho, dados in enumerate(matriz_adjacencia[no_atual]):
            if dados is not None:  # Se há uma conexão
                # Calcula o novo custo (soma de toll, fuel e distance_km)
                novo_custo = custo_atual + dados['toll'] + dados['fuel'] + dados['distance_km']

                # Se o vizinho não foi visitado ou encontramos um caminho mais barato
                if vizinho not in custos_minimos or novo_custo < custos_minimos[vizinho]:
                    custos_minimos[vizinho] = novo_custo
                    # Estimativa heurística (neste caso, usamos 0 por simplicidade)
                    heuristica = 0
                    custo_estimado = novo_custo + heuristica
                    # Adiciona o vizinho à fila de prioridade
                    heapq.heappush(fila, (custo_estimado, novo_custo, vizinho, caminho + [vizinho]))

    # Se não encontrou um caminho
    return None, float('inf')

# Função para calcular os custos individuais de um caminho
def calcular_custos_individuais(nome_ficheiro, matriz_adjacencia, mapa_nos, caminho):
    toll_total = 0
    fuel_total = 0
    distance_total = 0

    for i in range(len(caminho) - 1):
        origem_idx = mapa_nos[caminho[i]]
        destino_idx = mapa_nos[caminho[i + 1]]
        dados = matriz_adjacencia[origem_idx][destino_idx]
        toll_total += dados['toll']
        fuel_total += dados['fuel']
        distance_total += dados['distance_km']

    return toll_total, fuel_total, distance_total

nome_ficheiro, inicio, fim = importar_grafo_csv_3()
matriz_adjacencia, mapa_nos = importar_grafo_csv(nome_ficheiro)

# Encontrar o caminho de menor custo entre as cidades
caminho, custo_total = a_star(matriz_adjacencia, mapa_nos, inicio, fim)

# Exibir o resultado
if caminho:
    print(f"\nCaminho encontrado: {' -> '.join(caminho)}")
    print(f"Custo total: {custo_total}")

    # Calcular e exibir os custos individuais
    toll_total, fuel_total, distance_total = calcular_custos_individuais(nome_ficheiro, matriz_adjacencia, mapa_nos, caminho)
    print(f"Km Cost: {distance_total}")
    print(f"Toll Cost: {toll_total}")
    print(f"Fuel Cost: {fuel_total}")
else:
    print("\nNão foi possível encontrar um caminho.")
