from Router import Router
import sys
import random
from matrix_utils import *

def sendRandomPacket(routers: list[Router]):
    print("\nAttempt to send packet")
    fromRouter = routers[random.randint(1, len(routers) - 1)]
    toRouter = routers[random.randint(1, len(routers) - 1)]
    fromRouter.send_packet(fromRouter.create_packet(toRouter, "test_payload"))

def createNetwork(numRouters: int):

    #> creating a network of routers

    # creating routers
    routers: list[Router] = []
    for _ in range(numRouters):
        routers.append(Router())

    #> linking routers
    # linking each router linearly first (to gurantee connectedness)
    for i in range(1, numRouters):
        cost = random.randint(1, 10)
        routers[i].add_neighbor(routers[i-1], cost)
        routers[i-1].add_neighbor(routers[i], cost)

    # linking routers randomly
    minExtraConnections = numRouters // 2
    maxExtraConnections = max(int(numRouters * (numRouters - 1) / 2), minExtraConnections)
    for _ in range(random.randint(minExtraConnections, maxExtraConnections)):
        routerA: Router = routers[random.randint(0, numRouters - 1)]
        routerB: Router = routers[random.randint(0, numRouters - 1)]
        if routerA != routerB:
            cost = random.randint(1, 10)
            routerA.add_neighbor(routerB, cost)
            routerB.add_neighbor(routerA, cost)
    #< linking routers

    # printing adjacency matrix
    print("Current matrix:")
    print_adjacency_matrix(routers, create_adjacency_matrix(routers))

    sendRandomPacket(routers)

    removedRouter = routers.pop(random.randint(1, len(routers) - 1))
    removedRouter.disconnect()
    removedRouter2 = routers.pop(random.randint(1, len(routers) - 1))
    removedRouter2.disconnect()
    removedRouter3 = routers.pop(random.randint(1, len(routers) - 1))
    removedRouter3.disconnect()
    print(f"\nRemoving router {removedRouter}, {removedRouter2}, {removedRouter3}. New matrix:")
    print_adjacency_matrix(routers, create_adjacency_matrix(routers))

    sendRandomPacket(routers)
    sendRandomPacket(routers)
    sendRandomPacket(routers)
    sendRandomPacket(routers)
    #< creating a network of routers

if __name__ == "__main__":
    args = sys.argv[1:]

    numRouters = 0
    try:
        numRouters = len(args) > 0 and int(args[0]) or 2
    except:
        print("Invalid Arguments")
    
    createNetwork(numRouters)
    
    