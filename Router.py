from typing import TypedDict

currentRouterId = 0

class LSA(TypedDict):
    router: "Router"
    neighbors: dict["Router", int]

class packet(TypedDict):
    source: "Router"
    dest: "Router"
    payload: str
    pathCost: int
    hops: int

class Router:
    def __init__(self: "Router"):
        global currentRouterId

        self.id = currentRouterId
        currentRouterId += 1

        self.next_hop: dict[Router, Router] = {} # [destination, nextRouter]
        self.neighbors: dict[Router, int] = {} # [neighbor, cost]
        self.database: dict[Router, LSA] = {} # [router, lsa]

    def add_neighbor(self: "Router", router: "Router", cost: int):
        self.neighbors[router] = cost

    def create_lsa(self: "Router") -> LSA:
        return {
            "router": self,
            "neighbors": self.neighbors
        }

    def flood(self: "Router", lsa: LSA, sender = None):
        router = lsa["router"]

        if router not in self.database:
            self.database[router] = lsa

        for neighbor in self.neighbors:
            if neighbor != sender:
                neighbor.receive_lsa(lsa, self)

    def build_dijkstra(self: "Router"):
        pass
    def build_bellman_ford(self: "Router"):
        pass

    def receive_lsa(self: "Router", lsa: LSA, sender):
        router = lsa["router"]

        if router not in self.database:
            self.database[router] = lsa
            self.flood(lsa, sender)

    def send_packet(self: "Router", packet: packet):
        nextHopRouter = self.next_hop[packet.dest]

        packet.hops += 1
        packet.pathCost += self.neighbors[nextHopRouter]
        nextHopRouter.receive_packet(packet)

    def receive_packet(self: "Router", packet: packet):
        self.send_packet(packet)

    def __eq__(self: "Router", other):
        return self.id == other.id
    
    def __ne__(self: "Router", other):
        return self.id != other.id

    def __hash__(self: "Router"):
        return self.id