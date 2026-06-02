from collections import Counter

from createAgents import GenerateAgents
from graphCreation import ContactGraphBuilder
from clusterAssignment import ClusterAssigner


def report_clusters(agents, n_clusters: int) -> None:
    """Print each cluster's size and average attributes so we can sanity-check
    that the groups actually differ from one another."""
    print("\n=== cluster report ===")
    for cid in range(n_clusters):
        members = [a for a in agents if a.getClusterId() == cid]
        if not members:
            print(f"cluster {cid}: (empty)")
            continue

        n = len(members)
        avg_age = sum(a.getAttributes()["age"] for a in members) / n
        avg_risk = sum(a.getAttributes()["risk"] for a in members) / n
        avg_mob = sum(a.getAttributes()["mobility"] for a in members) / n
        pct_vax = 100 * sum(a.getAttributes()["vaccinated"] for a in members) / n

        print(
            f"cluster {cid}: n={n:3d} | "
            f"avg_age={avg_age:5.1f} | "
            f"avg_risk={avg_risk:.2f} | "
            f"avg_mobility={avg_mob:.2f} | "
            f"vaccinated={pct_vax:4.0f}%"
        )


def main():
    NUM_AGENTS = 200
    N_CLUSTERS = 4

    agents = GenerateAgents(NUM_AGENTS).createAgents()
    agents_by_id = {a.getAgentId(): a for a in agents}

    # assign clusters (replaces the random cluster_id from createAgents)
    assigner = ClusterAssigner(agents, n_clusters=N_CLUSTERS, seed=42)
    assigner.assign()

    # --- did the clustering work? ---
    print(f"cluster sizes: {assigner.clusterSizes()}")
    report_clusters(agents, N_CLUSTERS)

    # build the contact graph
    builder = ContactGraphBuilder(agents, avg_contacts=8, seed=42)
    graph = builder.build()

    print(f"\nnodes: {graph.number_of_nodes()}, edges: {graph.number_of_edges()}")
    sample_id = agents[0].getAgentId()
    print(f"agent {sample_id}: {agents_by_id[sample_id]}")
    print(f"  neighbors: {list(graph.neighbors(sample_id))}")


if __name__ == "__main__":
    main()