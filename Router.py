from typing import TypedDict

currentRouterId = 0

class LSA(TypedDict):
    sn: int
    router: "Router"
    neighbors: dict["Router", int]

class packet(TypedDict):
    source: "Router"
    dest: "Router"
    path: list["Router"]
    payload: str
    accumulated_cost: int
    accumulated_hops: int
    
def print_formatted_packet(packet: packet):
    print(
        f"Packet({packet['source']} -> {packet['dest']},  ",
        f"cost={packet['accumulated_cost']},  ",
        f"hops={packet['accumulated_hops']},  ",
        f"path={packet['path']})"
    )

class Router:
    def __init__(self: "Router"):
        global currentRouterId

        self.id: int = currentRouterId
        self.lsa_seq_num: int = 0
        currentRouterId += 1

        self.next_hop: dict[Router, Router] = {} # [destination, nextRouter]
        self.neighbors: dict[Router, int] = {} # [neighbor, cost]
        self.database: dict[Router, LSA] = {} # [router, lsa]

    def is_neighbor(self: "Router", other: "Router"):
        return other in self.neighbors
    
    def build_dijkstra(self: "Router"):
        # Distance from this router to every other router
        distance = {router: float("inf") for router in self.database}
        distance[self] = 0

        # Previous router in the shortest path
        previous = {}

        # Unvisited routers (make sure self is included even if not
        # explicitly a key in self.database)
        unvisited = set(self.database.keys())
        unvisited.add(self)

        while unvisited:
            # Pick unvisited router with smallest distance
            current = min(unvisited, key=lambda r: distance.get(r, float("inf")))
            unvisited.remove(current)

            # If remaining routers are unreachable, stop
            if distance[current] == float("inf"):
                break

            # Look at current router's neighbors from its LSA
            neighbors = self.database.get(current, {}).get("neighbors", {})
            for neighbor, cost in neighbors.items():
                if neighbor not in unvisited:
                    continue

                # Guard against neighbors we don't have a distance entry for
                if neighbor not in distance:
                    distance[neighbor] = float("inf")

                new_distance = distance[current] + cost

                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    previous[neighbor] = current

        # Build next_hop table
        self.next_hop.clear()

        for destination in distance:
            if destination == self:
                continue

            if destination not in previous:
                # No path exists
                continue

            # Walk backwards from destination until we reach self
            current = destination
            while previous[current] != self:
                current = previous[current]

            # current is now the first hop
            self.next_hop[destination] = current

    def build_bellman_ford(self: "Router"):
        pass

    def create_lsa(self: "Router") -> LSA:
        self.lsa_seq_num += 1
        lsa: LSA = {
            "sn": self.lsa_seq_num,
            "router": self,
            "neighbors": self.neighbors
        }
        self.database[self] = lsa
        return lsa
    def receive_lsa(self: "Router", lsa: LSA, sender):
        router = lsa["router"]
        
        if router in self.database:
            if self.database[router]["sn"] >= lsa["sn"]: # don't accept stale sequence numbers
                return
        
        self.database[router] = lsa
        self.flood(lsa, sender)

    def add_neighbor(self: "Router", router: "Router", cost: int):
        self.neighbors[router] = cost
        self.flood(self.create_lsa(), self)
    def remove_neighbor(self: "Router", router: "Router"):
        del self.neighbors[router]
        self.flood(self.create_lsa(), self)
    def get_neighbors(self: "Router") -> list["Router"]:
        return list(self.neighbors.keys())

    def flood(self: "Router", lsa: LSA, sender = None):
        router = lsa["router"]

        if router not in self.database:
            self.database[router] = lsa

        for neighbor in self.neighbors:
            if neighbor != sender:
                neighbor.receive_lsa(lsa, self)
        
        # build hop table at the end
        self.build_dijkstra()

    def create_packet(self: "Router", dest: "Router", payload: str) -> packet:
        return {
            "source": self,
            "dest": dest,
            "path": [],
            "payload": payload,
            "accumulated_cost": 0,
            "accumulated_hops": 0,
        }
    def send_packet(self: "Router", packet: packet):
        if packet["dest"] == self:
            print("Sending packet from and to the same router.")
            return
        if not packet["dest"] in self.next_hop:
            print(f"Cannot reach router {packet["dest"]} from router {self}")
            return
        nextHopRouter = self.next_hop[packet["dest"]]
        packet["path"].append(self)
        packet["accumulated_hops"] += 1
        packet["accumulated_cost"] += self.neighbors[nextHopRouter]
        nextHopRouter.receive_packet(packet)
    def receive_packet(self: "Router", packet: packet):
        if packet["dest"] == self:
            packet["path"].append(self)
            print_formatted_packet(packet)
        else:
            self.send_packet(packet)

    def disconnect(self: "Router"):
        # disconnecting all neighbors
        temp = self.neighbors
        self.neighbors = []

        for neighbor in temp:
            neighbor.remove_neighbor(self)


    def __eq__(self: "Router", other):
        otherId = -1
        if other:
            otherId = other.id
        return self.id == otherId
    def __ne__(self: "Router", other):
        otherId = -1
        if other:
            otherId = other.id
        return self.id != otherId
    
    def __str__(self: "Router"):
        return str(self.id)
        
    def __repr__(self):
        return str(self)

    def __hash__(self: "Router"):
        return self.id