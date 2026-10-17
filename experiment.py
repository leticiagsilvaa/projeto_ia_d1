import os
import matplotlib.pyplot as plt

from problem import GridPathfinding, GridState
from ids_tree import BFSTree, IDS


def run_experiments():
    grid_sizes = [3, 4, 5, 6, 7]

    results = {
        "BFS": {"expanded": [], "generated": [], "frontier": [], "time": []},
        "IDS": {"expanded": [], "generated": [], "frontier": [], "time": []}
    }

    print(f"{'Grid':<6} | {'Algoritmo':<9} | {'Prof. Sol.':<10} | {'Expandidos':<12} | {'Gerados':<12} | {'Max Fronteira':<13} | {'Tempo (s)':<10}")
    print("-" * 88)

    for n in grid_sizes:
        initial_state = GridState(0, 0)
        goal_state = GridState(n - 1, n - 1)

        problem = GridPathfinding(
            map_limits=(n, n),
            initial_state=initial_state,
            goal=goal_state,
            permite_diag=False
        )

        # 1. Executa BFS
        bfs = BFSTree(problem)
        res_bfs = bfs.search(initial_state)
        results["BFS"]["expanded"].append(res_bfs.metrics.nodes_expanded)
        results["BFS"]["generated"].append(res_bfs.metrics.nodes_generated)
        results["BFS"]["frontier"].append(res_bfs.metrics.max_frontier_size)
        results["BFS"]["time"].append(res_bfs.metrics.execution_time)

        depth_bfs = res_bfs.solution_node.depth if res_bfs.solution_node else -1
        print(f"{f'{n}x{n}':<6} | {'BFS':<9} | {depth_bfs:<10} | {res_bfs.metrics.nodes_expanded:<12} | {res_bfs.metrics.nodes_generated:<12} | {res_bfs.metrics.max_frontier_size:<13} | {res_bfs.metrics.execution_time:<10.5f}")

        # 2. Executa IDS
        ids = IDS(problem)
        res_ids = ids.search(initial_state)
        results["IDS"]["expanded"].append(res_ids.metrics.nodes_expanded)
        results["IDS"]["generated"].append(res_ids.metrics.nodes_generated)
        results["IDS"]["frontier"].append(res_ids.metrics.max_frontier_size)
        results["IDS"]["time"].append(res_ids.metrics.execution_time)

        depth_ids = res_ids.solution_node.depth if res_ids.solution_node else -1
        print(f"{f'{n}x{n}':<6} | {'IDS':<9} | {depth_ids:<10} | {res_ids.metrics.nodes_expanded:<12} | {res_ids.metrics.nodes_generated:<12} | {res_ids.metrics.max_frontier_size:<13} | {res_ids.metrics.execution_time:<10.5f}")
        print("-" * 88)

    plot_metrics(grid_sizes, results)


def plot_metrics(grid_sizes, results):
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Gráfico 1: Quantidade de Nós Gerados
    plt.figure(figsize=(8, 5))
    plt.plot(grid_sizes, results["BFS"]["generated"], marker='o', label='BFS (Tree-Search)')
    plt.plot(grid_sizes, results["IDS"]["generated"], marker='s', label='IDS (Tree-Search)')
    plt.title("Quantidade de Nós Gerados por Tamanho de Grid")
    plt.xlabel("Tamanho do Grid (N x N)")
    plt.ylabel("Nós Gerados")
    plt.xticks(grid_sizes)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_nos_gerados.png"), dpi=150)
    plt.close()

    # Gráfico 2: Tamanho Máximo da Fronteira
    plt.figure(figsize=(8, 5))
    plt.plot(grid_sizes, results["BFS"]["frontier"], marker='o', label='BFS (Tree-Search)')
    plt.plot(grid_sizes, results["IDS"]["frontier"], marker='s', label='IDS (Tree-Search)')
    plt.title("Tamanho Máximo da Fronteira (Memória) por Tamanho de Grid")
    plt.xlabel("Tamanho do Grid (N x N)")
    plt.ylabel("Tamanho Máximo da Fronteira (escala log)")
    plt.yscale("log")
    plt.xticks(grid_sizes)
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_fronteira_maxima.png"), dpi=150)
    plt.close()

    # Gráfico 3: Tempo de Execução
    plt.figure(figsize=(8, 5))
    plt.plot(grid_sizes, results["BFS"]["time"], marker='o', label='BFS (Tree-Search)')
    plt.plot(grid_sizes, results["IDS"]["time"], marker='s', label='IDS (Tree-Search)')
    plt.title("Tempo de Execução por Tamanho de Grid")
    plt.xlabel("Tamanho do Grid (N x N)")
    plt.ylabel("Tempo de Execução (s)")
    plt.xticks(grid_sizes)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_tempo_execucao.png"), dpi=150)
    plt.close()

    print(f"\nSucesso! Os 3 gráficos foram salvos na pasta: {output_dir}")


if __name__ == "__main__":
    run_experiments()