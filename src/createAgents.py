import random


class Agent:
    def __init__(self, agent_id: int, current_state: str, attributes: dict, cluster_id: int) -> None:
        self.agent_id = agent_id
        self.current_state = current_state
        self.attributes = attributes
        self.cluster_id = cluster_id

    def getAgentId(self) -> int:
        return self.agent_id

    def getCurrentState(self) -> str:
        return self.current_state

    def getAttributes(self) -> dict:
        return self.attributes

    def getClusterId(self) -> int:
        return self.cluster_id

    def setAgentId(self, newAgentId: int) -> None:
        self.agent_id = newAgentId

    def setCurrentState(self, current_state: str) -> None:
        self.current_state = current_state

    def setAttributes(self, attributes: dict) -> None:
        self.attributes = attributes

    def setClusterId(self, cluster_id: int) -> None:
        self.cluster_id = cluster_id

    def __str__(self) -> str:
        return (
            f"Agent(id={self.agent_id}, "
            f"state={self.current_state}, "
            f"cluster={self.cluster_id}, "
            f"attributes={self.attributes})"
        )

class GenerateAgents:
    def __init__(self, amountOfAgents: int):
        self.amountOfAgents = amountOfAgents
        self.createdAgents = []

    def createAgents(self) -> list[Agent]:
        possible_states = [
            "susceptible",
            "exposed",
            "infected",
            "recovered",
            "deceased"
        ]

        number_of_clusters = 4

        for agentNumber in range(self.amountOfAgents):

            random_state = random.choice(possible_states)

            random_attributes = {
                "age": random.randint(18, 90),
                "risk": round(random.uniform(0.0, 1.0), 2),
                "mobility": round(random.uniform(0.0, 1.0), 2),
                "vaccinated": random.choice([True, False])
            }

            random_cluster_id = random.randint(0, number_of_clusters - 1)

            new_agent = Agent(
                agent_id=agentNumber,
                current_state=random_state,
                attributes=random_attributes,
                cluster_id=random_cluster_id
            )

            self.createdAgents.append(new_agent)

        return self.createdAgents

    def getCreatedAgents(self) -> list[Agent]:
        return self.createdAgents


def debug():
    print("Debugging the creation of agents: ")

    agents = GenerateAgents(10)
    agentList = agents.createAgents()

    print(agentList[0])


if __name__ == "__main__":
    debug()