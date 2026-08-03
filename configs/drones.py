from hubs import HubNodes, HubType


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
        # print(f"curr_coords are {self.curr_coord}")
        self.finished = finished
        self.conn = None
        self.conn_wait = 0
        self.conn_turns = 0

        self.start_coord = (0, 0)
        self.target_coord = (0, 0)
        self.curr_coord = (0, 0)
        self.progress = 0
        self.moving = False

    def move(self):
        # print(f"drone is movig")
        if not self.moving:
            return

        frames = 0.0009

        if self.progress >= 1:
            if self.hub.hub_type == HubType.end_hub:
                self.finished = True
            self.progress = 1
            self.moving = False

        self.progress += frames

        start_x, start_y = self.start_coord
        target_x, target_y = self.target_coord

        x = start_x + (target_x - start_x) * self.progress
        y = start_y + (target_y - start_y) * self.progress

        if self.finished is False:
            self.curr_coord = (x, y)
