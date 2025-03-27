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
            
            for origem, destino, pedagio, combustivel, distancia in leitor:
                custo = float(pedagio) + float(combustivel)
                grafo[origem][destino] = custo
                cidades.update([origem, destino])
            
            return grafo, sorted(cidades)
            
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        print(f"Diretório atual: {os.getcwd()}")
        exit()

def distancia(cidade1, cidade2, grafo):
    """Distância entre cidades (custo direto ou heurística)"""
    if cidade2 in grafo[cidade1]:
        return grafo[cidade1][cidade2]
    return float('inf')  # Sem conexão direta

def expandir(grafo, arvore, cidade_alvo, max_passos=1000):
    """Expande uma árvore em direção a um alvo"""
    cidade_prox = min(arvore.keys(), key=lambda x: distancia(x, cidade_alvo, grafo))
    
    if cidade_prox == cidade_alvo:
        return cidade_alvo
    
    # Tenta encontrar conexão direta
    if cidade_alvo in grafo[cidade_prox]:
        custo = grafo[cidade_prox][cidade_alvo]
        if custo <= max_passos:
            arvore[cidade_alvo] = cidade_prox
            return cidade_alvo
    
    # Se não, escolhe uma cidade vizinha aleatória
    vizinhos = list(grafo[cidade_prox].keys())
    if not vizinhos:
        return cidade_prox
    
    cidade_nova = random.choice(vizinhos)
    arvore[cidade_nova] = cidade_prox
    return cidade_nova

def rrt_connect(grafo, inicio, objetivo, iteracoes=10000):
    """Implementação do RRT-Connect para encontrar caminho"""
    arvore_a = {inicio: None}
    arvore_b = {objetivo: None}
    
    for _ in range(iteracoes):
        # Expande árvore A
        cidade_aleatoria = random.choice(list(grafo.keys()))
        nova_a = expandir(grafo, arvore_a, cidade_aleatoria)
        
        # Expande árvore B em direção a nova_a
        nova_b = expandir(grafo, arvore_b, nova_a)
        
        # Verifica conexão
        if nova_b in arvore_a:
            caminho = []
            # Constrói caminho do início ao ponto de conexão
            cidade = nova_b
            while cidade is not None:
                caminho.append(cidade)
                cidade = arvore_a[cidade]
            caminho = caminho[::-1]
            
            # Adiciona do ponto de conexão ao objetivo
            cidade = arvore_b[nova_b]
            while cidade is not None:
                caminho.append(cidade)
                cidade = arvore_b[cidade]
            
            return caminho, calcular_custo(caminho, grafo)
        
        # Troca as árvores
        arvore_a, arvore_b = arvore_b, arvore_a
    
    return None, float('inf')

def calcular_custo(caminho, grafo):
    """Calcula o custo total do caminho"""
    custo_total = 0
    for i in range(len(caminho)-1):
        custo_total += grafo[caminho[i]][caminho[i+1]]
    return custo_total

def main():
    print("Sistema de Rotas com RRT-Connect")
    grafo, cidades = importar_grafo_csv('cidades.csv')
    
    print("\nCidades disponíveis:")
    for i, cidade in enumerate(cidades, 1):
        print(f"{i}. {cidade}")
    
    while True:
        try:
            inicio_idx = int(input("\nNúmero da cidade de início: ")) - 1
            fim_idx = int(input("Número da cidade de destino: ")) - 1
            inicio, fim = cidades[inicio_idx], cidades[fim_idx]
            break
        except (ValueError, IndexError):
            print("Entrada inválida. Tente novamente.")
    
    print(f"\nCalculando rota de {inicio} para {fim}...")
    caminho, custo = rrt_connect(grafo, inicio, fim)
    
    if caminho:
        print("\nRota encontrada:")
        print(" → ".join(caminho))
        print(f"Custo total: €{custo:.2f}")
    else:
        print("\nNão foi possível encontrar um caminho.")

if __name__ == "__main__":
    main()