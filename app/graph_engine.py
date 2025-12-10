# app/graph_engine.py

class Node:
    def __init__(self, name, func):
        self.name = name
        self.func = func


class Graph:
    def __init__(self, nodes, edges, loop_config=None):
        """
        nodes: dict[name -> Node]
        edges: dict[current_name -> next_name or None]
        loop_config: {
            "loop_node": "refine",
            "restart_from": "split",
            "condition": callable(state) -> bool,
            "max_loops": int
        }
        """
        self.nodes = nodes
        self.edges = edges
        self.loop_config = loop_config or {}

    def run(self, state):
        log = []

        # start from first node key
        current = list(self.nodes.keys())[0]

        loop_count = 0
        max_loops = self.loop_config.get("max_loops", 5)
        loop_node = self.loop_config.get("loop_node")
        restart_from = self.loop_config.get("restart_from")
        condition = self.loop_config.get("condition")

        while current:
            node = self.nodes[current]

            # run node function
            state = node.func(state)

            # record state after this node
            log.append({"node": current, "state": dict(state)})

            # default next node from edges
            next_node = self.edges.get(current)

            # generic looping logic
            if (
                condition is not None
                and current == loop_node
                and loop_count < max_loops
                and condition(state)
            ):
                # restart from beginning node
                next_node = restart_from
                loop_count += 1

            current = next_node

        return state, log


# in-memory stores
GRAPHS = {}
RUNS = {}
