from enum import Enum
from exceptions import ConfsError


class HubType(Enum):
    """
    enum class with the distinct hub types
    """
    start_hub = 'start_hub'
    end_hub = 'end_hub'
    hub = 'hub'
    connection = 'connection'


class ZoneType(Enum):
    """
    enum class with the distinct hub zone types
    """
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
        max_drones: int,
        conn_nodes: list["HubNodes"] | None = None,
        zone: ZoneType = ZoneType.normal,
        confs: list[str] = None,
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
        self.id = id
        self.hub_type = hub_type
        self.hub_name = hub_name
        self.coord = coord
        self.zone = zone
        self.confs = confs
        self.max_drones = max_drones
        self.drones = []
        self.level = level
        self.conn_nodes = [] if conn_nodes is None else conn_nodes
        self.connections = []
        self.grid_size = tuple[int, int]
        self.color = "green"
        self.extract_confs()
        self.map_drones()

    def print_node(self) -> None:
        """
        Auxiliar method for debugin
        prints node information
        """
        print(
            f"location is {self.hub_type.name} and "
            f"name is {self.hub_name} and coords are {self.coord}"
        )
        return None

    def extract_confs(self) -> None:
        """
        extracts confs metadata
        ensures no more metada is available
        """
        for conf in self.confs.split(' '):
            if "color" in conf.lower():
                self.color = conf.split('=')[1].lower()
            elif (
                "max_drones" in conf.lower()
            ):
                try:
                    m_d = int(conf.split('=')[1])
                    if self.hub_type.name not in ('start_hub', 'end_hub'):
                        self.max_drones = m_d
                except Exception:
                    raise ConfsError(
                        f"max_dones '{conf.split('=')[1]}' is not numeric"
                    )
                if m_d < 1:
                    raise ConfsError(f"max_dones {m_d} is lower than 0")
            elif "zone" in conf.lower():
                try:
                    self.zone = ZoneType[conf.split('=')[1].lower()]
                except Exception:
                    raise ConfsError(
                        f"Zone {conf.split('=')[1].lower()} does not exist"
                    )
            else:
                raise ConfsError(f"unkonw metadata {conf.lower()}")
        return None

    def map_drones(self) -> None:
        """
        maps the drones
        initially they all are on the start node
        """
        from drones import Drones
        if self.hub_type == HubType.start_hub:
            for i in range(self.max_drones):
                self.drones.append(
                    Drones(
                        id=i + 1,
                        hub=self
                    )
                )

    # def map_connections(self) -> None:
    #     for conn in self.confs.
