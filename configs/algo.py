from read_confs import ReadConfs
from hubs import HubNodes, ZoneType, HubType
from paths import Paths
from drones import Drones


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
        self.BFS()
        self.hub_validations()
        self.build_graph()
        self.hubs_w_drones = self.f_hubs_w_drones()
        self.sorted_paths = self.ordered_paths()

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

    def build_graph(self) -> None:
        for node in self.confs.hubs:
            self.graph[node] = node.conn_nodes

        return None

    @staticmethod
    def is_priority(path):
        for i, node in enumerate(path):
            priority = any(
                adj.zone == ZoneType.priority for adj in node.conn_nodes
                if len(adj.drones) < adj.max_drones
            )

            if (
                priority
                and (i + 1) < len(path)
                and path[i + 1].zone != ZoneType.priority
            ):
                return False

        return True

    @staticmethod
    def is_restricted(path):
        for i, node in enumerate(path):
            restricted = any(
                adj.zone == ZoneType.restricted for adj in node.conn_nodes
                if len(adj.drones) < adj.max_drones
            )

            if (
                restricted
                and (i + 1) < len(path)
                and path[i + 1].zone != ZoneType.restricted
            ):
                return False

        return True

    def find_all_paths(self, hub: HubNodes) -> None:
        def find_path(node, start, end, visited=None):
            if visited is None:
                visited = set()

            if (
                node in visited
                or len(start.drones) == 0
                or (
                    (len(node.drones) == node.max_drones and node != hub)
                    and node.hub_type not in (
                        HubType.start_hub, HubType.end_hub
                    ))
            ):
                return []

            visited = visited | {node}

            if node == end:
                return [[node]]

            paths = []
            # print(f"graph is {[_.hub_name for _ in self.graph]}")
            for adj_node in self.graph.get(node, []):
                for path in find_path(adj_node, start, end, visited):
                    paths.append([node] + path)

            return paths

        start = hub
        end = self.find_end()
        paths = find_path(start, start, end)
        for p in paths:
            self.all_paths.add(Paths(
                hubs=p,
                priority=self.is_priority(p),
                restricted=self.is_restricted(p)
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

    def ordered_paths(self) -> list[Paths]:

        self.all_paths = set()
        self.find_all_paths(self.find_start())

        sorted_paths = sorted(
            self.all_paths, key=lambda x: x.priority, reverse=True
        )
        sorted_paths = sorted(sorted_paths, key=lambda x: x.cost)

        return sorted_paths

    def f_hubs_w_drones(self) -> None:
        for hub in self.confs.hubs:
            for drone in hub.drones:
                drone.moved = False
        hubs_w_drones = filter(lambda x: len(x.drones) > 0, self.confs.hubs)
        hubs_w_drones = [
            hub for hub in list(hubs_w_drones)
            if hub.hub_type != HubType.end_hub
        ]
        return hubs_w_drones

    def move_drones_hubs(
            self,
            drone: Drones,
            hubs: list[HubNodes],
            next: bool
    ) -> tuple[bool, list[str]]:
        log = []
        for idx_h, hub in enumerate(hubs):
            if drone.hub != hub:
                continue
            else:
                idx_d = hub.drones.index(drone)

            if (next is False):
                continue

            if drone.coord != drone.hub.coord:
                drone.in_conn = True
                drone.progress = 0
                drone.moving = True
                continue
            else:
                self.in_conn = False

            if (
                drone.hub == hub
                and drone.moved is False
            ):
                conn = [
                    _ for _ in self.confs.all_connections
                    if (
                        _.start == hubs[idx_h].hub_name
                        and _.end == hubs[idx_h + 1].hub_name
                    )
                ][0]

                if conn.pass_drones == conn.max_drones:
                    continue

                if hubs[idx_h + 1].hub_type == HubType.end_hub:
                    drone.finished = True

                drone.prev_hub = drone.hub
                drone.hub = hubs[idx_h + 1]

                hubs[idx_h + 1].drones.append(drone)
                log.append(
                        f"D{drone.id}-"
                        f"{hubs[idx_h + 1].hub_name}"
                    )
                hubs[idx_h].drones.pop(idx_d)
                drone.conn_turns += 1

                conn.pass_drones += 1
                drone.moved = True
                next = False
                drone.progress = 0
                drone.moving = True

                break
        return next, log

    # def move_drones_conns(
    #         self,
    #         drone: Drones
    # ) -> list[str]:
    #     log = []
    #     # print("-----------------")

    #     conn = drone.conn
    #     hub_end = [
    #         _ for _ in self.confs.hubs if _.hub_name == drone.conn.end
    #     ]

    #     hub_end = hub_end[0]
    #     if len(hub_end.drones) == hub_end.max_drones:
    #         raise ("shit in max drones. Need another protection")
    #     hub_end.drones.append(drone)
    #     conn.drones.pop(conn.drones.index(drone))
    #     conn.pass_drones = len(conn.drones)
    #     drone.conn = None
    #     return log
    def reset_conns(self):
        for _ in self.confs.all_connections:
            _.pass_drones = 0

    def walk_one(
            self,
            drones: list[Drones],
            type: str = 'hub'
    ) -> list[str]:

        log = []
        paths = self.sorted_paths
        self.reset_conns()

        for drone in drones:
            next = True
            for path in paths:

                if len(drones) == 0:
                    break

                # validate drones in hubs
                next, this_log = self.move_drones_hubs(
                    drone, path.hubs, next
                )
                log.extend(this_log)

        return log

    def find_drones_h(self) -> list[Drones]:
        drones = self.confs.all_drones
        for drone in drones:
            drone.moved = False

        drones = [
            drone for drone in sorted(drones, key=lambda x: x.id)
            if drone.finished is False
        ]
        return drones

    def walk(self) -> None:
        log = []

        drones_hubs = self.find_drones_h()
        # drones_hubs = list(
        #     drones_hubs
        # )

        if len(drones_hubs) != 0:
            # print(f"drones_hubs are {drones_hubs}")
            log.extend(self.walk_one(drones_hubs))
        if len(log):
            print(" ".join(log))

        return None
