import random
import networkx as nx

class ContactGraphBuilder:
    def __init__(self, agents: list, avg_contacts: int = 8, seed: int = None) -> None:
        self.agents = agents
        self.avg_contacts = avg_contacts          # average degree you want
        self.rng = random.Random(seed)
        self.graph = nx.Graph()                   # undirected

    def build(self) -> nx.Graph:
        ids = [a.getAgentId() for a in self.agents]

        # 1) one node per agent; store the STATIC attributes on the node
        for agent in self.agents:
            self.graph.add_node(agent.getAgentId(), **agent.getAttributes())

        # 2) wire up edges. Pick endpoints with probability weighted by mobility,
        #    so active agents accumulate more contacts (the +0.1 stops anyone
        #    from being completely isolated).
        weights = [a.getAttributes()["mobility"] + 0.1 for a in self.agents]
        n = len(ids)
        target_edges = int(self.avg_contacts * n / 2)

        added, attempts = 0, 0
        while added < target_edges and attempts < target_edges * 20:
            a, b = self.rng.choices(ids, weights=weights, k=2)
            attempts += 1
            if a != b and not self.graph.has_edge(a, b):
                self.graph.add_edge(a, b)
                added += 1

        return self.graph

    def getGraph(self) -> nx.Graph:
        return self.graph

    def infected_neighbor_count(self, agent_id: int, agents_by_id: dict) -> int:
        """How many of this agent's contacts are currently infected."""
        return sum(
            1 for nbr in self.graph.neighbors(agent_id)
            if agents_by_id[nbr].getCurrentState() == "infected"
        )