import itertools
import time
import re
import os

def ler_matriz_arquivo(caminho_arquivo):
    """
    Lê uma matriz de adjacência de um arquivo .txt.
    """
    matriz = []
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            if linha.strip():  # ignora linhas em branco
                valores = list(map(float, linha.split()))
                matriz.append(valores)
    return matriz

def extrair_custo_otimo(nome_arquivo):
    """
    Extrai o custo ótimo do nome do arquivo.
    """
    match = re.search(r'_(\d+)\.txt$', nome_arquivo)
    if match:
        return float(match.group(1))
    return None

def calcular_custo_rota(matriz, rota):
    """
    Calcula o custo total de uma rota, incluindo o retorno à cidade inicial.
    """
    custo = 0
    for i in range(len(rota) - 1):
        custo += matriz[rota[i]][rota[i + 1]]
    custo += matriz[rota[-1]][rota[0]]  # retorno à cidade inicial
    return custo

def tsp_forca_bruta(matriz):
    """
    Resolve o problema do caixeiro viajante por força bruta.
    Retorna a melhor rota e seu custo.
    """
    n = len(matriz)
    vertices = list(range(n))
    melhor_custo = float('inf')
    melhor_rota = None
    
    for perm in itertools.permutations(vertices[1:]):  # fixa o vértice 0
        rota = [0] + list(perm)
        custo = calcular_custo_rota(matriz, rota)
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_rota = rota

    return melhor_rota, melhor_custo


if __name__ == "__main__":
    # Pasta onde estão as instâncias no repositório (observe o nome correto 'instances')
    pasta_instancias = "instancias"
    arquivo = input("Digite o nome do arquivo TSP (ex: tsp1_253.txt, tsp2_1248.txt, tsp3_1194.txt, tsp4_7013.txt, tsp5_27603.txt): ").strip()

    # monta o caminho completo de forma portável
    caminho_completo = os.path.join(pasta_instancias, arquivo)

    print("\nLendo matriz...")
    try:
        matriz = ler_matriz_arquivo(caminho_completo)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_completo}")
        print("Verifique o nome do arquivo (por exemplo, cuidado com 'tsp' vs 'tps') e se a pasta 'instances' existe.")
        raise

    custo_otimo = extrair_custo_otimo(arquivo)

    print(f"\nNúmero de vértices: {len(matriz)}")
    print(f"Custo ótimo esperado (extraído do nome do arquivo): {custo_otimo if custo_otimo else 'Não informado'}")

    print("\nExecutando algoritmo exato (força bruta)...")
    inicio = time.time()
    rota, custo_calculado = tsp_forca_bruta(matriz)
    fim = time.time()
    tempo_execucao = fim - inicio

    # Calcula erro percentual se custo ótimo for conhecido
    if custo_otimo:
        erro_percentual = ((custo_calculado - custo_otimo) / custo_otimo) * 100
    else:
        erro_percentual = None

    print("\n--- RESULTADOS ---")
    print(f"Melhor rota encontrada: {rota}")
    print(f"Custo calculado: {custo_calculado:.2f}")
    if custo_otimo:
        print(f"Custo ótimo (esperado): {custo_otimo:.2f}")
        print(f"Erro percentual: {erro_percentual:.2f}%")
    print(f"Tempo de execução: {tempo_execucao:.8f} segundos")
