import csv
import os
import random
import math
from collections import defaultdict

def importar_grafo_csv(nome_arquivo):
    """Importa o grafo do CSV e retorna a estrutura de adjacência"""
    try:
        caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
        with open(caminho, newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)  # Pular cabeçalho
            
            grafo = defaultdict(dict)
            cidades = set()
            
            for linha in leitor:
                origem, destino, pedagio, combustivel, distancia = linha
                grafo[origem][destino] = {
                    'toll': float(pedagio),
                    'fuel': float(combustivel),
                    'distance': float(distancia)
                }
                cidades.update([origem, destino])
            
            return grafo, sorted(cidades)
            
    except FileNotFoundError:
        print(f"\nERRO: Arquivo '{nome_arquivo}' não encontrado.")
        print(f"Diretório atual: {os.path.dirname(__file__)}")
        exit()

def calcular_custo_composto(origem, destino, grafo, pesos):
    """Calcula custo composto entre duas cidades"""
    if destino not in grafo[origem]:
        return float('inf')
    dados = grafo[origem][destino]
    return (pesos['toll'] * dados['toll'] + 
            pesos['fuel'] * dados['fuel'] + 
            pesos['distance'] * dados['distance'])

def expandir(grafo, arvore, cidade_alvo, pesos, max_passos=1000):
    """Expande uma árvore em direção a um alvo considerando custo composto"""
    # Encontra a cidade mais próxima na árvore (menor custo composto)
    cidade_prox = min(arvore.keys(),
                     key=lambda x: calcular_custo_composto(x, cidade_alvo, grafo, pesos))
    
    if cidade_prox == cidade_alvo:
        return cidade_alvo
    
    # Tenta conectar diretamente
    if cidade_alvo in grafo[cidade_prox]:
        custo = calcular_custo_composto(cidade_prox, cidade_alvo, grafo, pesos)
        if custo <= max_passos:
            arvore[cidade_alvo] = cidade_prox
            return cidade_alvo
    
    # Se não, escolhe o melhor vizinho (menor custo composto)
    vizinhos = list(grafo[cidade_prox].keys())
    if not vizinhos:
        return cidade_prox
    
    # Escolhe o vizinho com menor custo em direção ao alvo
    cidade_nova = min(vizinhos,
                     key=lambda x: calcular_custo_composto(cidade_prox, x, grafo, pesos) + 
                                 calcular_custo_composto(x, cidade_alvo, grafo, pesos))
    
    arvore[cidade_nova] = cidade_prox
    return cidade_nova

def rrt_connect_otimizado(grafo, inicio, objetivo, pesos, iteracoes=5000):
    """RRT-Connect otimizado para múltiplos objetivos"""
    arvore_a = {inicio: None}
    arvore_b = {objetivo: None}
    melhor_caminho = None
    melhor_custo = float('inf')
    melhores_custos_individuais = None
    
    for _ in range(iteracoes):
        # 80% de chance de expandir em direção ao objetivo
        if random.random() < 0.8:
            cidade_alvo = objetivo if random.random() < 0.5 else inicio
        else:
            cidade_alvo = random.choice(list(grafo.keys()))
        
        # Expande ambas as árvores
        nova_a = expandir(grafo, arvore_a, cidade_alvo, pesos)
        nova_b = expandir(grafo, arvore_b, cidade_alvo, pesos)
        
        # Verifica conexão
        if nova_a in arvore_b:
            caminho = reconstruir_caminho(arvore_a, arvore_b, nova_a)
            custo, custos_ind = calcular_custos_totais(caminho, grafo)
            if custo < melhor_custo:
                melhor_caminho = caminho
                melhor_custo = custo
                melhores_custos_individuais = custos_ind
        
        if nova_b in arvore_a:
            caminho = reconstruir_caminho(arvore_a, arvore_b, nova_b)
            custo, custos_ind = calcular_custos_totais(caminho, grafo)
            if custo < melhor_custo:
                melhor_caminho = caminho
                melhor_custo = custo
                melhores_custos_individuais = custos_ind
        
        # Troca as árvores para balancear
        arvore_a, arvore_b = arvore_b, arvore_a
    
    return melhor_caminho, melhor_custo, melhores_custos_individuais

def reconstruir_caminho(arvore_a, arvore_b, ponto_conexao):
    """Reconstrói o caminho completo a partir das duas árvores"""
    caminho = []
    # Parte da árvore A (início até conexão)
    cidade = ponto_conexao
    while cidade is not None:
        caminho.append(cidade)
        cidade = arvore_a.get(cidade, None)
    caminho = caminho[::-1]
    
    # Parte da árvore B (conexão até objetivo)
    cidade = arvore_b[ponto_conexao]
    while cidade is not None:
        caminho.append(cidade)
        cidade = arvore_b.get(cidade, None)
    
    return caminho

def calcular_custos_totais(caminho, grafo):
    """Calcula todos os custos do caminho"""
    toll_total = fuel_total = distance_total = 0
    for i in range(len(caminho)-1):
        dados = grafo[caminho[i]][caminho[i+1]]
        toll_total += dados['toll']
        fuel_total += dados['fuel']
        distance_total += dados['distance']
    
    custo_composto = toll_total + fuel_total + distance_total
    custos_individuais = {
        'toll': toll_total,
        'fuel': fuel_total,
        'distance': distance_total
    }
    return custo_composto, custos_individuais

def main():
    print("Sistema de Rotas com RRT-Connect Otimizado")
    
    # Solicitar arquivo CSV
    nome_arquivo = input("Digite o nome do arquivo CSV (ex: cidades.csv): ")
    grafo, cidades = importar_grafo_csv(nome_arquivo)
    
    # Configurar pesos
    print("\nDefina os pesos para cada fator (soma deve ser 1.0):")
    pesos = {
        'toll': float(input("Peso para pedágio (0-1): ")),
        'fuel': float(input("Peso para combustível (0-1): ")),
        'distance': float(input("Peso para distância (0-1): "))
    }
    
    # Mostrar cidades disponíveis
    print("\nCidades disponíveis:")
    for i, cidade in enumerate(cidades, 1):
        print(f"{i}. {cidade}")
    
    # Solicitar cidades de início e destino
    inicio_idx = int(input("\nNúmero da cidade de início: ")) - 1
    fim_idx = int(input("Número da cidade de destino: ")) - 1
    inicio, fim = cidades[inicio_idx], cidades[fim_idx]
    
    # Executar algoritmo
    print(f"\nCalculando rota de {inicio} para {fim}...")
    caminho, custo_total, custos_ind = rrt_connect_otimizado(grafo, inicio, fim, pesos)
    
    # Mostrar resultados
    if caminho:
        print("\n🌟 Melhor Rota Encontrada:")
        print(" → ".join(caminho))
        print("\n📊 Custos Totais:")
        print(f"Pedágio: €{custos_ind['toll']:.2f}")
        print(f"Combustível: €{custos_ind['fuel']:.2f}")
        print(f"Distância: {custos_ind['distance']:.1f} km")
        print(f"\n💰 Custo Composto: {custo_total:.2f}")
    else:
        print("\nNão foi possível encontrar uma rota válida.")

if __name__ == "__main__":
    main()