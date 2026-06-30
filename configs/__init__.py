from abc import ABC
from enum import Enum
# from typing import Optional


class HubType(Enum):
    start_hub = 'start_hub'
    end_hub = 'end_hub'
    hub = 'hub'


class ZoneType(Enum):
    normal = 'normal'
    blocked = 'blocked'
    restricted = 'restricted'
    priority = 'priority'


class GarphNodes(ABC):
    def __init__(
        self,
        hub_type: HubType,
        hub_name: str,
        coord: tuple[int, int],
        zone: ZoneType = ZoneType.normal,
        color: str = None,
        max_drones: int = 1
    ):
        self.hub_type = hub_type
        self.hub_name = hub_name
        self.coord = coord
        self.zone = zone
        self.color = color
        self.max_drones = max_drones


# class GarphNodes(ABC):
#     def __init__(
#         self,
#         hub_type: HubType,
#         hub_name: str,
#         coord: tuple[int, int],
#         zone: ZoneType = ZoneType.normal,
#         color: str = None,
#         max_drones: int = 1
#     ):
#         self.hub_type = hub_type
#         self.hub_name = hub_name
#         self.coord = coord
#         self.zone = zone
#         self.color = color
#         self.max_drones = max_drones


class ReadConfs(ABC):
    def __init__(
            self,
            file_path
    ):
        self.valid = 0
        self.file_path = file_path
        self.file_info = None
        self.nodes = list[GarphNodes]
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
                    print(line.split(":")[0])
                    if isinstance(line.split(":")[0], ZoneType):
                        print("is in instance\n\n\n\n\n\n\n\n")
                    print(line)
                    print()
                    line = fd.readline()
        except FileNotFoundError as e:
            print(e)


if __name__ == '__main__':
    confs = ReadConfs('./maps/easy/01_linear_path.txt')
    print(confs.nb_drones)
