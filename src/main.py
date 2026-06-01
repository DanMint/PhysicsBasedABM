from createAgents import GenerateAgents
from graphCreation import ContactGraphBuilder


def main():
    # 1) create the population
    NUM_AGENTS = 200
    agents = GenerateAgents(NUM_AGENTS).createAgents()

    # lookup so we can turn a neighbor's id (what the graph stores)
    # back into the agent object (where the live state lives)
    agents_by_id = {a.getAgentId(): a for a in agents}

    # 2) build the contact graph from those agents
    builder = ContactGraphBuilder(agents, avg_contacts=8, seed=42)
    graph = builder.build()

    # 3) sanity check
    print(f"agents: {len(agents)}")
    print(f"nodes:  {graph.number_of_nodes()}")
    print(f"edges:  {graph.number_of_edges()}")
    print(f"avg degree: {2 * graph.number_of_edges() / graph.number_of_nodes():.1f}")

    # look at one agent and its neighbors
    sample_id = agents[0].getAgentId()
    neighbors = list(graph.neighbors(sample_id))
    print(f"\nagent {sample_id}: {agents_by_id[sample_id]}")
    print(f"  neighbors: {neighbors}")
    print(f"  infected neighbors: {builder.infected_neighbor_count(sample_id, agents_by_id)}")


if __name__ == "__main__":
    main()