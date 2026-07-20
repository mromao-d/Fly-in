from hubs import HubNodes


class Drones:
    def __init__(
        self,
        id: int,
        hub: HubNodes,
        # conns: list[ConnectionNodes]
    ):
        self.id = id
        self.hub = hub
