from collections import Counter

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class ClusterAssigner:
    def __init__(self, agents: list, n_clusters: int = 4, seed: int = None) -> None:
        self.agents = agents
        self.n_clusters = n_clusters
        self.seed = seed
        self.model = None
        self.scaler = None
        self.feature_names = ["age", "risk", "mobility", "vaccinated"]

    def _featurize(self) -> np.ndarray:
        """Turn each agent's attributes into a numeric feature row."""
        rows = []
        for agent in self.agents:
            attr = agent.getAttributes()
            rows.append([
                attr["age"],
                attr["risk"],
                attr["mobility"],
                1.0 if attr["vaccinated"] else 0.0,   # bool -> number
            ])
        return np.array(rows, dtype=float)

    def assign(self) -> list:
        features = self._featurize()

        # Standardize first: age is 18-90 while risk/mobility are 0-1.
        # Without this, KMeans distance is dominated by age and the other
        # attributes barely matter.
        self.scaler = StandardScaler()
        scaled = self.scaler.fit_transform(features)

        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.seed,
            n_init=10,
        )
        labels = self.model.fit_predict(scaled)

        # Write the cluster id back onto each agent (overrides the random one).
        for agent, label in zip(self.agents, labels):
            agent.setClusterId(int(label))

        return self.agents

    def getModel(self) -> KMeans:
        return self.model

    def clusterSizes(self) -> dict:
        return dict(sorted(Counter(a.getClusterId() for a in self.agents).items()))


def debug():
    print("Debugging the clustering of agents: ")

    from createAgents import GenerateAgents

    agents = GenerateAgents(200).createAgents()
    assigner = ClusterAssigner(agents, n_clusters=4, seed=42)
    assigner.assign()

    print(f"cluster sizes: {assigner.clusterSizes()}")
    for agent in agents[:3]:
        print(f"  {agent}")


if __name__ == "__main__":
    debug()