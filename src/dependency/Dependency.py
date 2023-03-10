from typing import Union
from ..definitions.Trigger import Trigger
from ..definitions.Procedure import Procedure
from ..definitions.Table import Table
from typing import List
import graphviz

class Dependency:
    def __init__(self, parsed) -> None:
        self.parsed = parsed
        self.dot = graphviz.Digraph(comment='Dependency', format='svg')
        self.edges = {}
       # self.dot.graph_attr['layout'] = 'neato'

    """
    Solve the entire Dependency Graph.
    """
    def solve(self):
        dependency = []
        visited = {}
        max_depth = float('inf')
        prune = False
        for i in self.parsed.procedure_graph.values():
            self._resolve_dependency(i, dependency, visited, self.dot, max_depth=max_depth, prune=prune)
        for i in self.parsed.table_graph.values():
            self._resolve_dependency(i, dependency, visited, self.dot, max_depth=max_depth, prune=prune)
        return dependency

    def plot(self, procedure: str=None, table=None, max_depth=float('inf'), prune=False):
        dependency = []
        visited = {}
        seed = None
        if procedure is not None:
            seed = self.parsed.procedure_graph[procedure.upper()]
        elif table is not None:
            seed = self.parsed.table_graph[table.upper()]

        if seed is None:
            raise Exception("Need to set table or procedure")
        self._resolve_dependency(seed, dependency, visited, self.dot, max_depth=max_depth, prune=prune)
        self.dot.render('dependency')

        return dependency

    def get_procedure_dependency(self, procedure: str, max_depth=float('inf'), prune=False):
        # 1. First we need to know all tables
        # 2. Then we need to know all procedures
        # 3. Then we need to know all triggers
        dependency = []
        visited = {}
        procedure = self.parsed.procedure_graph[procedure.upper()]
        self._resolve_dependency(procedure, dependency, visited, max_depth=max_depth, prune=prune)
        return dependency

    def _resolve_dependency(self, item: Union[Trigger, Procedure, Table], dependency: List[str], visited, dot=None, max_depth=float('inf'), prune=False):
        if isinstance(item, Procedure):
            self._plot_dot(dot, lambda: dot.node(item.name, item.name, color="blue"))
        elif isinstance(item, Trigger):
            self._plot_dot(dot, lambda: dot.node(item.name, item.name, shape="box", color="red"))
        else:
            self._plot_dot(dot, lambda: dot.node(item.name, item.name, color="black"))

        if max_depth <= 0:
            # We hit the max depth
            return

        if isinstance(item, Trigger) or  isinstance(item, Procedure):
            revisit_tables = []
            for i in item.references_tables:
                if i not in visited:
                    self._plot_dot(dot, lambda: dot.edge(item.name.upper(), i.reference.upper()))
                    visited[i] = True
                    revisit_tables.append(i)
                    try:
                        self._resolve_dependency(
                            self.parsed.table_graph[i.reference.upper()].get_state_type((i.type if prune else None)),
                            dependency,
                            visited,
                            dot,
                            max_depth=max_depth - 1,
                            prune=prune,
                        )
                    except Exception as e:
                        print(e)

            for i in item.references_procedures:
                if i not in visited:
                    self._plot_dot(dot, lambda: dot.edge(item.name.upper(), i.upper()))
                    visited[i] = True
                    try:
                        self._resolve_dependency(
                            self.parsed.procedure_graph[i.upper()],
                            dependency,
                            visited,
                            dot,
                            max_depth=max_depth - 1,
                            prune=prune,
                        )
                    except Exception as e:
                        print(e)
        else:
            for i in item.triggers:
                # it's a reference type
                if i.name not in visited:
                    self._plot_dot(dot, lambda: dot.edge(item.name.upper(), i.name.upper()))
                    visited[i.name] = True
                    try:
                        self._resolve_dependency(
                            i,
                            dependency,
                            visited,
                            dot,
                            max_depth=max_depth - 1,
                            prune=prune,
                        )
                    except Exception as e:
                        print(e)

        dependency.append(item)

    def _plot_dot(self, dot, func):
        if dot is not None:
            func()
