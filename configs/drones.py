from hubs import HubNodes


class Drones:
    def __init__(
        self,
        id: int,
        hub: "HubNodes",
        moved: bool = False,
        finished: bool = False,
    ):
        self.id = id
        self.hub = hub
        self.moved = moved
        self.finished = finished
        self.conn = None
        self.conn_wait = 0
        self.conn_turns = 0
