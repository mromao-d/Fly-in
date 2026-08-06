import re
from .hubs import HubType, HubNodes
from .connection_nodes import ConnectionNodes
from .drones import Drones
from .exceptions import ConfsError


class ReadConfs:
    """
    main part of the program
    reads and treats the confs
    """
    def __init__(
            self,
            file_path: str
    ):
        """
        inits class
        Args: file path
        """
        self.file_path: str = file_path
        self.file_info = None
        self.hubs: list[HubNodes] = []
        self.all_connections: list[ConnectionNodes] = []
        self.all_drones: list[Drones] = []
        self.nb_drones = 0
        self.parse_txt()
        self.normalize_coords()
        self.map_coords()
        self.map_hub_conns()
        self.map_conn_coords()
        self.map_drones()
        self.val_connections()
        # self.map_connections()
        # self.map_b_hub_conns()

    def file_exists(self) -> None:
        """
        validates if file exists in path
        """
        try:
            with open(self.file_path):
                pass
            return None

        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.file_path} not found")

    def parse_txt(self):
        """
        reads the file and extracts the configs
        """
        self.file_exists()
        with open(self.file_path) as fd:
            line = fd.readline()
            line = fd.readline()
            if "nb_drones" in line:
                aux_d = line.split("nb_drones: ")
                if len(aux_d) != 2:
                    raise ConfsError("wrong config for nb drones")
                self.nb_drones = int(aux_d[-1])
            else:
                raise ConfsError("First line must contain number of drones")
            if self.nb_drones < 1:
                raise ConfsError("number of drones must be > 0")
            line = fd.readline()
            while (line):
                try:
                    hub = HubType(line.split(":")[0])
                    confs = re.search(r"\[(.*?)\]", line)
                    if confs:
                        confs = confs.group(1)
                    name = line.split(" ")[1].strip('\n')

                    if hub == HubType.connection:
                        connection = ConnectionNodes(
                            path=name,
                            confs=confs
                        )
                        self.all_connections.append(connection)
                    else:
                        coords = (
                            int(line.split()[2]), int(line.split()[3])
                        )
                        max_drones = self.nb_drones if (
                            self.nb_drones
                            and hub in [HubType.start_hub, HubType.end_hub]
                        ) else 1

                        node = HubNodes(
                            hub_type=hub,
                            hub_name=name,
                            coord=coords,
                            confs=confs,
                            max_drones=max_drones
                            )
                        self.hubs.append(
                            node
                        )
                except ValueError:
                    pass
                finally:
                    line = fd.readline()

    def normalize_coords(self):
        """
        Normalization of hub coords for visualization purposes
        (I dont want them to be < 0)
        """
        hubs = self.hubs
        coords = [hub.coord for hub in hubs]
        min_x = min(x for (x, y) in coords)
        min_y = min(y for (x, y) in coords)
        dx = -min_x if min_x else 0
        dy = -min_y if min_y else 0
        for hub in hubs:
            x, y = hub.coord
            hub.coord = (x + dx, y + dy)

    def map_coords(self):
        """
        Gives the map dimensions, based on the coords of the hubs
        """
        hubs = self.hubs
        coords = [hub.coord for hub in hubs]

        min_x = min(x for (x, y) in coords)
        max_x = max(x for (x, y) in coords)
        min_y = min(y for (x, y) in coords)
        max_y = max(y for (x, y) in coords)

        map_x = max_x - min_x
        map_y = max_y - min_y
        if map_x < 0 or map_y < 0 or map_x == 0 and map_y == 0:
            raise ValueError("Map dimensions must be greater than 0")
        self.grid_size = ((max_x - min_x), (max_y - min_y))

    def map_hub_conns(self):
        """
        Maps the forward hubs for each hub
        """
        for hub in self.hubs:
            f_hubs = []
            connections = [
                conn.end for conn in self.all_connections
                if (
                    conn.start == hub.hub_name
                    # and conn.max_link_capacity > 0
                )
            ]

            f_hubs = [
                front_hub for front_hub in self.hubs
                if front_hub.hub_name in connections
            ]

            hub.conn_nodes.extend(f_hubs)

            conns = [
                conn for conn in self.all_connections
                if conn.start == hub.hub_name
            ]

            hub.connections.extend(conns)

    def map_conn_coords(self) -> None:
        """
        maps all connection coords
        """
        for conn in self.all_connections:
            start_node = [_ for _ in self.hubs if _.hub_name == conn.start][0]
            end_node = [_ for _ in self.hubs if _.hub_name == conn.end][0]

            conn.coord = (
                abs(start_node.coord[0] + end_node.coord[0]) / 2,
                abs(start_node.coord[1] + end_node.coord[1]) / 2
            )

        return None

    def map_drones(self) -> None:
        """
        maps all drones that are in the start hub to confs
        """
        start = [_ for _ in self.hubs if _.hub_type == HubType.start_hub][0]

        for drone in start.drones:
            drone.start_coord = start.coord
            drone.target_coord = start.coord
            drone.curr_coord = start.coord
            self.all_drones.append(drone)

    def val_connections(self) -> None:
        """
        Validates if connections confs such as:
            - same start and end
            - working both ways
        """
        conns = []
        for conn in self.all_connections:
            if conn.start == conn.end:
                raise ConfsError(
                    f"Start and end have the same value: {conn.end}"
                )
            sort = sorted([conn.start, conn.end])
            conns.extend([sort])
        for _ in conns:
            if len(
                list(
                    filter(lambda x: x == _, conns)
                )
            ) > 1:
                raise ConfsError(
                    f"This conn works both ways: {_}"
                )

        return None
