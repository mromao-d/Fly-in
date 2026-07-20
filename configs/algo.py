from read_confs import ReadConfs
from hubs import HubNodes, ZoneType, HubType
from drones import Drones
from paths import Paths


class Algo:
    def __init__(self, confs: ReadConfs):
        """
        Inits the graph class
        Args:
            V: int = #Hubs (or #vertices)

        inits:
            adj: list[list[Edges]] = list adj hubs
            level: int = level of the node
        """
        self.all_paths: list[Paths] = []
        self.confs = confs
        self.finish = False
        self.graph = {}
        # self.paths: list[HubNodes] = []
        self.map_drones()
        self.BFS()
        self.hub_validations()
        # self.DFS()
        self.build_graph()
        # self.walk()

    def find_start(self) -> HubNodes | None:
        start = next(
            (
                hub for hub in self.confs.hubs
                if hub.hub_type.value == 'start_hub'
            ),
            None
        )
        return start

    def find_end(self) -> HubNodes | None:
        end = next(
            (
                hub for hub in self.confs.hubs
                if hub.hub_type.value == 'end_hub'
            ),
            None
        )
        return end

    def map_drones(self):
        total = sum([len(el.drones) for el in self.confs.hubs])
        if total == 0:
            start_node = self.find_start()
            for i in range(self.confs.nb_drones):
                start_node.drones.append(
                    Drones(
                        id=i + 1,
                        hub=start_node
                    )
                )
                # print(f"mapping for D{i}")
        # print(f"total is {total}")

    def BFS(self) -> None:
        start = self.find_start()
        if start:
            q = [start]
            visited = set()
            start.level = 0
            q.append(start)

            while q:
                hub = q.pop(0)

                for adj in hub.conn_nodes:
                    if adj in visited or adj.zone.name == 'blocked':
                        continue

                    if adj.hub_type.value == 'end_hub':
                        self.finish = True

                    adj.level = hub.level + 1

                    q.append(adj)
                    visited.add(adj)

        return None

    # def DFS(self) -> None:
    #     start = self.find_start()
    #     if start is None:
    #         return None
    #     path = [start]
    #     visited = set()
    #     visited.add(start)
    #     end = False
    #     while path and end is False:
    #         hub = path[-1]
    #         if len(hub.conn_nodes) == 0:
    #             path.pop()
    #         elif all(x in visited for x in hub.conn_nodes):
    #             path.pop()
    #         else:
    #             for adj in sorted(hub.conn_nodes, key=lambda x: x.zone.value):
    #                 if (adj in visited or adj.zone.name == 'blocked'):
    #                     continue

    #                 # elif adj.level >= hub.level:

    #                 elif adj.hub_type.value == 'end_hub':
    #                     path.append(adj)
    #                     end = True
    #                     break

    #                 else:
    #                     path.append(adj)
    #                     visited.add(adj)
    #                     break

    #     # bottle = min([hub.max_drones for hub in path])
    #     # sorted_path = sorted(path, key = lambda x: x.zone.value)
    #     # print(f"path is {[(hub.hub_name, hub.zone.value) for hub in path]} for {str(bottle)} drones")
    #     return None

    def build_graph(self) -> None:
        for node in self.confs.hubs:
            self.graph[node] = node.conn_nodes

        return None

    @staticmethod
    def is_priority(path):
        for i, node in enumerate(path):
            priority = any(
                adj.zone == ZoneType.priority for adj in node.conn_nodes
            )

            if (
                priority
                and (i + 1) < len(path)
                and path[i + 1].zone != ZoneType.priority
            ):
                return False

        return True

    def find_all_paths(self, hub: HubNodes) -> None:
        def find_path(node, end, visited=None):
            if visited is None:
                visited = set()

            if node in visited or (
                len(node.drones) == node.max_drones
                and node.hub_type not in (HubType.start_hub, HubType.end_hub)
            ):
                return []

            visited = visited | {node}

            if node == end:
                return [[node]]

            paths = []

            for adj_node in self.graph.get(node, []):
                for path in find_path(adj_node, end, visited):
                    paths.append([node] + path)

            return paths

        start = hub
        end = self.find_end()
        paths = find_path(start, end)
        for p in paths:
            self.all_paths.append(Paths(
                path=p,
                priority=self.is_priority(p)
                # priority=False
            ))
        return None

    def hub_validations(self) -> None:
        if self.finish is False:
            raise Exception("Map is not linked between start and end")
        for hub in self.confs.hubs:
            hubs = list(
                filter(lambda x: x.hub_name == hub.hub_name, self.confs.hubs)
            )
            if len(hubs) > 1:
                raise Exception(f"More than one hub called {hub.hub_name}")

        return None

    def ordered_paths(self, hubs_w_drones: list[HubNodes]) -> list[Paths]:

        for hub in hubs_w_drones:
            self.find_all_paths(hub)

        # print("here 2")
        # print(f"all paths are {self.all_paths}")
        priority_paths = [p for p in self.all_paths if p.priority]
        # priority_paths = [hub.hub_name for hub in [path for path in paths]]
        # print()

        # print(f"priority_paths are {priority_paths}")
        # print(f"priority_paths 2 are {[[hub.hub_name for hub in el.path] for el in priority_paths]} with cost {[el.cost for el in priority_paths]}")
        # print()

        sorted_paths = sorted(priority_paths, key=lambda x: x.cost)
        # print(f"sorted_paths are {sorted_paths}")
        # print(f"sorted_paths 2 are {[[hub.hub_name for hub in el.path] for el in sorted_paths]} with cost {[el.cost for el in sorted_paths]}")
        return sorted_paths
        # print(f"priority_paths 2 are {[[hub.hub_name for hub in el] for el in priority_paths]}")
        # priority_paths = sorted(priority_paths, key=lambda x: x.cost)
        # print(priority_paths)
        # print([_.hub_name for _ in hubs_w_drones])
        # print([_.path for _ in paths])
        # # for hub in self.confs.hubs:
        # #     if len(hub.drones) > 0:
        # #         print(f"hub {hub.hub_name} has {len(hub.drones)} drones")
        # # for _ in self.paths:
        # #     print(_)
        # # print(self.paths)
        # # print(f"{self.paths} are self.paths")
        # priority_paths = [el for el in self.paths if el.priority is True]
        # print(f"priority_paths are {priority_paths}")
        # # print()
        # for _ in priority_paths:
        #     for hub in _.path:
        #         print(hub.hub_name)
        # print([[hub.hub_name for hub in path.path] for path in priority_paths])
        # print("end")
        # # # print(_.path for _ in priority_paths])

    def walk(self):
        import time
        time.sleep(2)
        self.all_paths = []
        hubs_w_drones = filter(lambda x: len(x.drones) > 0, self.confs.hubs)
        hubs_w_drones = [
            hub for hub in list(hubs_w_drones)
            if hub.hub_type != HubType.end_hub
        ]
        # print(f"hubs_w_drones are {len(hubs_w_drones)} {[_.drones for _ in hubs_w_drones]}")
        # print()
        # print(f"hubs_w_drones are {hubs_w_drones}")
        paths = self.ordered_paths(hubs_w_drones)
        while True:
            if len(paths) == 0:
                print("no more movements")
                break
            if sum(len(_.drones) for _ in hubs_w_drones) == 0:
                print("no more drones")
                break
            print(f"path is {[hub.hub_name for hub in paths[0].path]}")
            paths[0].path[1].drones.append(paths[0].path[0].drones[0])
            paths[0].path[0].drones.pop()
            break
