import time
import re
import os

def ler_matriz_arquivo(caminho_arquivo):
    matriz = []
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            if linha.strip():
                valores = list(map(float, linha.split()))
                matriz.append(valores)
    return matriz

def extrair_custo_otimo(nome_arquivo):
    match = re.search(r'_(\d+)\.txt$', nome_arquivo)
    if match:
        return float(match.group(1))
    return None

def calcular_custo_rota(matriz, rota):
    custo = 0
    for i in range(len(rota) - 1):
        custo += matriz[rota[i]][rota[i + 1]]
    custo += matriz[rota[-1]][rota[0]]  # retorna ao início
    return custo

# --- Implementação do Kruskal ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        raiz_u = self.find(u)
        raiz_v = self.find(v)
        if raiz_u != raiz_v:
            if self.rank[raiz_u] < self.rank[raiz_v]:
                self.parent[raiz_u] = raiz_v
            elif self.rank[raiz_u] > self.rank[raiz_v]:
                self.parent[raiz_v] = raiz_u
            else:
                self.parent[raiz_v] = raiz_u
                self.rank[raiz_u] += 1

def kruskal_mst(matriz):
    n = len(matriz)
    arestas = []

    # Cria lista de arestas (peso, u, v)
    for i in range(n):
        for j in range(i + 1, n):
            arestas.append((matriz[i][j], i, j))

    # Ordena por peso
    arestas.sort(key=lambda x: x[0])

    uf = UnionFind(n)
    mst = [[] for _ in range(n)]  # lista de adjacência da MST

    for peso, u, v in arestas:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst[u].append(v)
            mst[v].append(u)

    return mst

# --- DFS para gerar rota aproximada ---
def dfs_mst(mst, inicio=0):
    visitado = [False] * len(mst)
    rota = []

    def dfs(u):
        visitado[u] = True
        rota.append(u)
        for v in mst[u]:
            if not visitado[v]:
                dfs(v)

    dfs(inicio)
    return rota

def tsp_aproximado_mst(matriz):
    mst = kruskal_mst(matriz)
    rota = dfs_mst(mst, inicio=0)
    custo = calcular_custo_rota(matriz, rota)
    return rota, custo

# --- Programa principal ---
if __name__ == "__main__":
    pasta_instancias = "instancias"
    arquivo = input("Digite o nome do arquivo TSP (ex: tsp1_253.txt, tsp2_1248.txt, tsp3_1194.txt, tsp4_7013.txt, tsp5_27603.txt): ").strip()
    caminho_completo = os.path.join(pasta_instancias, arquivo)

    print("\nLendo matriz...")
    try:
        matriz = ler_matriz_arquivo(caminho_completo)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_completo}")
        raise

    custo_otimo = extrair_custo_otimo(arquivo)

    print(f"\nNúmero de vértices: {len(matriz)}")
    print(f"Custo ótimo esperado: {custo_otimo if custo_otimo else 'Desconhecido'}")

    print("\nExecutando algoritmo aproximativo (MST - Kruskal)...")
    inicio = time.time()
    rota, custo_calculado = tsp_aproximado_mst(matriz)
    fim = time.time()
    tempo_execucao = fim - inicio

    if custo_otimo:
        erro_percentual = ((custo_calculado - custo_otimo) / custo_otimo) * 100
    else:
        erro_percentual = None

    print("\n--- RESULTADOS ---")
    print(f"Rota aproximada: {rota}")
    print(f"Custo calculado: {custo_calculado:.2f}")
    if custo_otimo:
        print(f"Custo ótimo (esperado): {custo_otimo:.2f}")
        print(f"Erro percentual: {erro_percentual:.2f}%")
    print(f"Tempo de execução: {tempo_execucao:.8f} segundos")
