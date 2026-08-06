from .hubs import HubNodes, HubType


class Drones:
    """
    drones class that will go through the graph
    """
    def __init__(
        self,
        id: int,
        hub: "HubNodes",
        moved: bool = False,
        finished: bool = False,
    ):
        """
        inits class
        Args:
            id (int): id of the drone (from 1 to nb_drones)
            hub (HubNodes): current hub node
            moved (bool): if drone has moved in current turn
            finished (bool): if drone has reached final hub
        """
        from .connection_nodes import ConnectionNodes
        self.id = id
        self.hub = hub
        self.moved = moved
        # print(f"curr_coords are {self.curr_coord}")
        self.finished = finished
        self.conn: ConnectionNodes | None = None
        self.conn_wait = 0
        self.conn_turns = 0
        # self.cost = 0

        self.start_coord: tuple[float, float] = (0, 0)
        self.target_coord: tuple[float, float] = (0, 0)
        self.curr_coord: tuple[float, float] = (0, 0)
        self.progress: float = 0
        self.moving = False

    def move(self) -> None:
        """
        simulates movement of the drone
        between a start position and an end position
        """
        if not self.moving:
            return

        frames = 0.009

        if self.progress >= 1:
            if self.hub.hub_type == HubType.end_hub:
                self.finished = True
            self.start_coord = self.target_coord
            self.progress = 1
            self.moving = False

        self.progress += frames

        start_x, start_y = self.start_coord
        target_x, target_y = self.target_coord

        x = start_x + (target_x - start_x) * self.progress
        y = start_y + (target_y - start_y) * self.progress

        if self.finished is False:
            self.curr_coord = (x, y)

        return None
