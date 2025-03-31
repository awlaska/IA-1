import csv
import heapq

def importar_grafo_csv(nome_ficheiro):
    mapa_nos = {}
    arestas = []

    try:
        with open("../"+nome_ficheiro, newline='', encoding='utf-8') as ficheiro:
            leitor = csv.reader(ficheiro)
            next(leitor)  # Ignorar cabeçalho

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

    except FileNotFoundError:
        print(f"Erro: O ficheiro '{nome_ficheiro}' não foi encontrado.")
        exit()


import heapq

def a_star_todos_caminhos(matriz_adjacencia, mapa_nos, inicio, fim):
    if inicio not in mapa_nos or fim not in mapa_nos:
        raise ValueError("Cidade de início ou fim não encontrada no mapa.")

    inicio_idx = mapa_nos[inicio]
    fim_idx = mapa_nos[fim]

    fila = [(0, 0, inicio_idx, [inicio_idx])]  # (Custo estimado, Custo real, Nó atual, Caminho percorrido)
    caminhos = []
    visitados = set()  # Conjunto para evitar ciclos e loops infinitos

    while fila:
        custo_estimado, custo_atual, no_atual, caminho = heapq.heappop(fila)

        if no_atual == fim_idx:
            caminhos.append((caminho, custo_atual))
            continue

        if no_atual in visitados:
            continue  # Pula se já foi visitado

        visitados.add(no_atual)

        for vizinho, dados in enumerate(matriz_adjacencia[no_atual]):
            if dados is not None and vizinho not in caminho:  # Evita revisitar
                novo_custo = custo_atual + dados['toll'] + dados['fuel'] + dados['distance_km']
                heapq.heappush(fila, (novo_custo, novo_custo, vizinho, caminho + [vizinho]))

    return caminhos



def calcular_custos_individuais(matriz_adjacencia, caminho):
    toll_total, fuel_total, distance_total = 0, 0, 0

    for i in range(len(caminho) - 1):
        origem_idx, destino_idx = caminho[i], caminho[i + 1]
        dados = matriz_adjacencia[origem_idx][destino_idx]
        toll_total += dados['toll']
        fuel_total += dados['fuel']
        distance_total += dados['distance_km']

    return toll_total, fuel_total, distance_total


def importar_grafo_csv_3():
    choice = -1
    while choice != "0":
        choice = input("Escolha o arquivo CSV:\n1. cidades.csv\n2. graph3.csv\n3. graph3_2.csv\n- ")

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

        elif choice == "0":
            print("Saindo do menu.")
            return None, None, None

        else:
            print("Escolha inválida. Tente novamente.")


# Chamar o menu para o usuário escolher o arquivo e cidades
nome_ficheiro, inicio, fim = importar_grafo_csv_3()

if nome_ficheiro and inicio and fim:
    # Continuar com o carregamento do grafo e cálculo do caminho, por exemplo
    matriz, mapa_nos = importar_grafo_csv(nome_ficheiro)
    caminhos = a_star_todos_caminhos(matriz, mapa_nos, inicio, fim)

    if caminhos:
        print(f"\nForam encontrados {len(caminhos)} caminhos:")
        for i, (caminho, custo_total) in enumerate(caminhos, 1):
            caminho_cidades = [list(mapa_nos.keys())[idx] for idx in caminho]
            toll_total, fuel_total, distance_total = calcular_custos_individuais(matriz, caminho)
            print(f"\nCaminho {i}: {' -> '.join(caminho_cidades)}")
            print(f"Custo total: {custo_total}")
            print(f"Distância total: {distance_total} km")
            print(f"Pedágio total: {toll_total}")
            print(f"Combustível total: {fuel_total}")
    else:
        print("\nNão foi possível encontrar um caminho.")
