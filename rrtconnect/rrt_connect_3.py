import csv
from heapq import heappop, heappush

def importar_grafo_csv(nome_arquivo):
    mapa_nos = {}
    arestas = []
    
    with open(nome_arquivo, newline='', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)  # Pular cabeçalho
        
        for linha in leitor:
            origem, destino, pedagio, combustivel, distancia = linha
            arestas.append((origem, destino, float(pedagio) + float(combustivel)))  # Soma pedágio + combustível como custo
            
            if origem not in mapa_nos:
                mapa_nos[origem] = len(mapa_nos)
            if destino not in mapa_nos:
                mapa_nos[destino] = len(mapa_nos)
    
    # Criar matriz de adjacência com custos
    tamanho = len(mapa_nos)
    matriz = [[float('inf')] * tamanho for _ in range(tamanho)]
    
    for origem, destino, custo in arestas:
        i, j = mapa_nos[origem], mapa_nos[destino]
        matriz[i][j] = custo
    
    return matriz, mapa_nos

def dijkstra(matriz, mapa_nos, inicio, fim):
    tamanho = len(mapa_nos)
    idx_inicio = mapa_nos[inicio]
    idx_fim = mapa_nos[fim]
    
    distancias = [float('inf')] * tamanho
    distancias[idx_inicio] = 0
    predecessores = [None] * tamanho
    fila_prioridade = [(0, idx_inicio)]
    
    while fila_prioridade:
        dist_atual, idx_atual = heappop(fila_prioridade)
        
        if idx_atual == idx_fim:
            break
        
        if dist_atual > distancias[idx_atual]:
            continue
        
        for vizinho in range(tamanho):
            custo = matriz[idx_atual][vizinho]
            if custo != float('inf'):
                dist = dist_atual + custo
                if dist < distancias[vizinho]:
                    distancias[vizinho] = dist
                    predecessores[vizinho] = idx_atual
                    heappush(fila_prioridade, (dist, vizinho))
    
    # Reconstruir caminho
    caminho = []
    idx_atual = idx_fim
    while idx_atual is not None:
        caminho.append(idx_atual)
        idx_atual = predecessores[idx_atual]
    caminho.reverse()
    
    # Converter índices para nomes de cidades
    mapa_inverso = {v: k for k, v in mapa_nos.items()}
    caminho_cidades = [mapa_inverso[idx] for idx in caminho]
    
    return caminho_cidades, distancias[idx_fim]

def main():
    print("Sistema de Rotas Entre Cidades Europeias")
    print("Carregando dados...")
    
    matriz, mapa_nos = importar_grafo_csv('cidades.csv')
    cidades = sorted(mapa_nos.keys())
    
    print("\nCidades disponíveis:")
    for i, cidade in enumerate(cidades, 1):
        print(f"{i}. {cidade}")
    
    while True:
        try:
            inicio_idx = int(input("\nDigite o número da cidade de início: ")) - 1
            fim_idx = int(input("Digite o número da cidade de destino: ")) - 1
            cidade_inicio = cidades[inicio_idx]
            cidade_fim = cidades[fim_idx]
            break
        except (ValueError, IndexError):
            print("Entrada inválida. Por favor, digite números correspondentes às cidades listadas.")
    
    print(f"\nCalculando rota de {cidade_inicio} para {cidade_fim}...")
    caminho, custo_total = dijkstra(matriz, mapa_nos, cidade_inicio, cidade_fim)
    
    if custo_total == float('inf'):
        print("\nNão existe caminho entre as cidades selecionadas.")
    else:
        print("\nMelhor caminho encontrado:")
        print(" -> ".join(caminho))
        print(f"\nCusto total (pedágio + combustível): €{custo_total:.2f}")

if __name__ == "__main__":
    main()