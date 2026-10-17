import time
from collections import deque

from search_lib.core import (
    SearchNode,
    SearchStrategy,
    State,
    SearchMetrics,
    SearchResult,
    Problem
)
from search_lib.algorithms.dls_tree import DLS


class BFSTree(SearchStrategy):
    """Busca em Largura em Árvore (Tree-BFS)."""

    def search(self, initial_state: State) -> SearchResult:
        start_time = time.perf_counter()
        metrics = SearchMetrics()

        root = SearchNode(initial_state)
        metrics.nodes_generated += 1

        frontier = deque([root])
        metrics.max_frontier_size = len(frontier)

        while frontier:
            node = frontier.popleft()
            metrics.nodes_expanded += 1

            if self.problem.is_goal(node.state):
                metrics.execution_time = time.perf_counter() - start_time
                return SearchResult(solution_node=node, metrics=metrics)

            for action in self.problem.actions(node.state):
                res_action = action.apply(node.state)
                if res_action is not None:
                    next_state, action_cost = res_action
                    child = SearchNode(
                        state=next_state,
                        parent=node,
                        action=action,
                        cost=node.cost + action_cost
                    )
                    metrics.nodes_generated += 1
                    frontier.append(child)
                    if len(frontier) > metrics.max_frontier_size:
                        metrics.max_frontier_size = len(frontier)

        metrics.execution_time = time.perf_counter() - start_time
        return SearchResult(solution_node=None, metrics=metrics)


class IDS(SearchStrategy):
    """Busca por Aprofundamento Iterativo em Árvore (Tree-IDS)."""

    def __init__(self, problem: Problem, max_depth: int = 100):
        super().__init__(problem)
        self.max_depth = max_depth

    def search(self, initial_state: State) -> SearchResult:
        start_time = time.perf_counter()
        total_metrics = SearchMetrics()

        for depth_limit in range(self.max_depth + 1):
            dls = DLS(self.problem, depth_limit=depth_limit)
            res = dls.search(initial_state)

            total_metrics.nodes_expanded += res.metrics.nodes_expanded
            total_metrics.nodes_generated += res.metrics.nodes_generated
            total_metrics.max_frontier_size = max(
                total_metrics.max_frontier_size,
                res.metrics.max_frontier_size
            )

            if res.solution_node is not None:
                total_metrics.execution_time = time.perf_counter() - start_time
                return SearchResult(solution_node=res.solution_node, metrics=total_metrics)

        total_metrics.execution_time = time.perf_counter() - start_time
        return SearchResult(solution_node=None, metrics=total_metrics)