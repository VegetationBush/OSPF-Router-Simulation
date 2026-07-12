from network import Network
import time

networkSizes = [10, 20, 30, 40, 50, 60, 70]
approximateAverageConnections = [2, 4, 6, 8, 10, 12, 14]
approximteConnectedness = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
sendPackets = 50

result = []

for networkSize in networkSizes:
    for averageConnections in approximateAverageConnections:
        for connectedness in approximteConnectedness:
            newNetwork = Network(networkSize, averageConnections, max(1, int(connectedness * networkSize)))
            
            cumHops = 0
            cumCost = 0

            print("Waiting for network to build routing table")
            time.sleep(0.1) # waiting for network to build jump tables

            for _ in range(sendPackets):
                returnedPacket = newNetwork.send_random_packet()
                cumHops += returnedPacket["accumulated_hops"]
                cumCost += returnedPacket["accumulated_cost"]

            result.append(
                {
                    "networkSize": networkSize,
                    "averageConnections": averageConnections,
                    "connectedness": connectedness,
                    "averageHops": cumHops / sendPackets,
                    "averageCost": cumCost / sendPackets,
                }
            )

print(result)

"""
Generating plot using line graphs
merges graphs with the same dependent variable together
"""

import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(result)

independent_vars = ["networkSize", "averageConnections", "connectedness"]
dependent_vars = ["averageHops", "averageCost"]

fig, axes = plt.subplots(1, len(independent_vars), figsize=(16, 5), sharey=False)

for ax, indep in zip(axes, independent_vars):
    grouped = df.groupby(indep)[dependent_vars].mean().reset_index().sort_values(indep)

    ax.plot(grouped[indep], grouped["averageHops"], marker='o', linewidth=2, label="averageHops")
    ax.plot(grouped[indep], grouped["averageCost"], marker='s', linewidth=2, label="averageCost")

    ax.set_xlabel(indep)
    ax.set_ylabel("value")
    ax.set_title(f"Hops & Cost vs {indep}")
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()