from abc import ABC, abstractmethod
from enum import Enum
import re
# from typing import Optional


class ConnectionNodes:
    def __init__(
        self,
        path: str
    ):
        self.path = path
        self.start = None
        self.end = None
        self.split_path()

    def split_path(self):
        self.start = self.path.split('-')[0]
        self.end = self.path.split('-')[1]


class HubType(Enum):
    start_hub = 'start_hub'
    end_hub = 'end_hub'
    hub = 'hub'
    connection = 'connection'


class ZoneType(Enum):
    normal = 'normal'
    blocked = 'blocked'
    restricted = 'restricted'
    priority = 'priority'


class GarphNodes:
    def __init__(
        self,
        hub_type: HubType,
        hub_name: str,
        coord: tuple[int, int],
        conn_nodes: ConnectionNodes = None,
        zone: ZoneType = ZoneType.normal,
        confs: list[str] = None,
        max_drones: int = 1
    ):
        self.hub_type = hub_type
        self.hub_name = hub_name
        self.coord = coord
        self.zone = zone
        self.confs = confs
        self.max_drones = max_drones
        self.conn_nodes = conn_nodes

    def print_node(self):
        print(f"location is {self.hub_type.name} and name is {self.hub_name}")


class ReadConfs:
    def __init__(
            self,
            file_path
    ):
        self.valid = 0
        self.file_path:str = file_path
        self.file_info = None
        self.graph: list[GarphNodes] = []
        self.connection: list[ConnectionNodes] = []
        self.nb_drones = 0
        self.parse_txt()
        # self.file_info = self.file_exists()
        # self.read_file()

    def file_exists(self) -> None:
        try:
            with open(self.file_path):
                pass
            return None

        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.file_path} not found")

    def parse_txt(self):
        try:
            self.file_exists()
            with open(self.file_path) as fd:
                line = fd.readline()
                while (line):
                    if "nb_drones" in line:
                        self.nb_drones = line.split("nb_drones: ")[-1]
                    try:
                        hub = HubType(line.split(":")[0])
                        confs = re.search(r"\[(.*?)\]", line)
                        name = line.split(" ")[1].strip('\n')

                        if hub == HubType.connection:
                            node = ConnectionNodes(path=name)
                            self.connection.append(node)
                        else:
                            node = GarphNodes(
                                hub_type=hub,
                                hub_name=name,
                                coord=(0,1),
                                confs=confs
                                )
                            print(f"HubType.connection.value is {HubType.connection.value} and hub is {hub}")
                            self.graph.append(
                                node
                            )
                    except ValueError as e:
                        # print(e)
                        pass
                    except Exception as e:
                        print(f"{type(e).__name__} | {e}")
                    finally:
                        line = fd.readline()
        except FileNotFoundError as e:
            print(e)


if __name__ == '__main__':
    confs = ReadConfs('./maps/easy/01_linear_path.txt')
    # print(confs.nodes)
    for node in confs.graph:
        # print(node)
        node.print_node()
    print()
    for node in confs.connection:
        print(node.path)
