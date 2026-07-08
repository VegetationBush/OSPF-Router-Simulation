from Router import Router
import sys
import random

def initNetwork(numRouters: int):

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
    for _ in range(random.randint(numRouters // 2, numRouters * 2)):
        routerA: Router = routers[random.randint(0, numRouters - 1)]
        routerB: Router = routers[random.randint(0, numRouters - 1)]
        if routerA != routerB:
            cost = random.randint(1, 10)
            routerA.add_neighbor(routerB, cost)
            routerB.add_neighbor(routerA, cost)
    #< linking routers

    # flooding routers
    routers[0].flood(routers[0].create_lsa())
    
    #< creating a network of routers

if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        numRouters = args[0] and int(args[0]) or 2
        if numRouters < 2:
            print("Number of routers must be >= 2")
        else:
            initNetwork(numRouters)
    except:
        print("Invalid Arguments")
        pass
    
    