from hubs import HubNodes, ZoneType


class Drones:
    def __init__(
        self,
        id: int,
        hub: "HubNodes",
        time: int,
        moved: bool = False,
        finished: bool = False,
    ):
        self.id = id
        self.hub = hub
        self.prev_hub = hub
        self.moved = moved
        self.finished = finished
        self.time = time
        self.in_conn = False
        self.moving = True
        self.progress = 0
        self.coord = self.prev_hub.coord
        self.conn = None
        self.conn_wait = 0
        self.conn_turns = 0

    def move(self):
        frames = 0.001
        if not self.moving:
            return

        if self.hub.zone == ZoneType.restricted:
            frames /= 2
            if self.progress >= 0.5:
                self.progress = 0.5
                self.moving = False
        self.progress += frames

        if self.progress >= 1:
            self.progress = 1
            self.moving = False

        if self.in_conn is True:
            print(f"drone in conn")
            start_x = abs(self.hub.coord[0] - self.prev_hub.coord[0]) / 2
            start_y = abs(self.hub.coord[1] - self.prev_hub.coord[1]) / 2

        else:
            start_x, start_y = self.prev_hub.coord
        end_x, end_y = self.hub.coord

        x = start_x + (end_x - start_x) * self.progress
        y = start_y + (end_y - start_y) * self.progress

        self.coord = (x, y)
