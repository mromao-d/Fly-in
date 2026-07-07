from enum import Enum


class HubType(Enum):
    start_hub = 'start_hub'
    end_hub = 'end_hub'
    hub = 'hub'
    connection = 'connection'


class ZoneType(Enum):
    normal = 1
    blocked = -1
    restricted = 2
    priority = 0


# need to validate if there is start and end
class HubNodes:
    def __init__(
        self,
        hub_type: HubType,
        hub_name: str,
        coord: tuple[int, int],
        drones: int,
        conn_nodes: list["HubNodes"] | None = None,
        b_conn_nodes: list["HubNodes"] | None = None,
        zone: ZoneType = ZoneType.normal,
        confs: list[str] = None,
        max_drones: int = 1,
        level: int = -1
    ):
        """
        inits each node of the graph (treated as Hub)

        Args:
            hub_type: Enum = start, hun or end
            coord: tuple[int] = coordenates
            conn_nodes: list[ConnectionNodes] = forward nodes
            zone: Enum = zone types
            confs: list[str] = list of confs between '[]'
            max_drones: int = max drones allowed at the same time
        """
        self.hub_type = hub_type
        self.hub_name = hub_name
        self.coord = coord
        self.zone = zone
        self.confs = confs
        self.max_drones = max_drones
        self.drones = drones
        self.level = level
        self.conn_nodes = [] if conn_nodes is None else conn_nodes
        self.b_conn_nodes = [] if b_conn_nodes is None else b_conn_nodes
        self.grid_size = tuple[int, int]
        self.color = "green"
        self.extract_confs()

    def print_node(self):
        print(f"location is {self.hub_type.name} and name is {self.hub_name} and coords are {self.coord}")

    def extract_confs(self):
        for conf in self.confs.split(' '):
            if "color" in conf.lower():
                self.color = conf.split('=')[1].lower()
            if "max_drones" in conf.lower():
                self.max_drones = conf.split('=')[1]
            if "zone" in conf.lower():
                self.zone = ZoneType[conf.split('=')[1].lower()]
