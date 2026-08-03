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

        sorted_paths = sorted(self.all_paths, key=lambda x: x.cost)
        sorted_paths = sorted(
            sorted_paths, key=lambda x: x.priority, reverse=True
        )

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

    # def connections_w_drones(self) -> list[ConnectionNodes]:
    #     for conn in self.confs.all_connections:
    #         conn.pass_drones = len(conn.drones)
    #     connections = [
    #         _ for _ in self.confs.all_connections if len(_.drones) > 0
    #     ]

    #     return connections

    def move_drones_hubs(
            self,
            drone: Drones,
            hubs: list[HubNodes],
            next: bool
    ) -> tuple[bool, list[str]]:
        log = []
        for idx_h, hub in enumerate(hubs):

            try:
                idx_d = hub.drones.index(drone)
            except ValueError:
                continue

            if (
                next is False
                or len(hubs[idx_h + 1].drones) == hubs[idx_h + 1].max_drones
            ):
                continue

            if (
                drone in hub.drones
                and drone.moved is False
            ):
                conn = [
                    _ for _ in self.confs.all_connections
                    if (
                        _.start == hubs[idx_h].hub_name
                        and _.end == hubs[idx_h + 1].hub_name
                    )
                ][0]
                # if conn.path == 'fast_path-merge_point':
                #     print(f"conn pass drones is {conn.pass_drones} and max capacity is {conn.max_drones}")

                if conn.pass_drones == conn.max_drones:
                    continue

                if (
                    hubs[idx_h + 1].zone == ZoneType.restricted
                    and conn.pass_drones < conn.max_drones
                ):
                    log.append(
                            f"D{drone.id}-{conn.end}"
                        )

                    drone.start_coord = drone.target_coord
                    drone.target_coord = conn.coord

                    conn.drones.append(drone)
                    hubs[idx_h].drones.pop(idx_d)
                    drone.conn = conn
                    drone.conn_wait += 2
                    drone.conn_turns += 2
                else:
                    hubs[idx_h + 1].drones.append(drone)
                    log.append(
                            f"D{drone.id}-"
                            f"{hubs[idx_h + 1].hub_name}"
                        )

                    drone.start_coord = drone.target_coord
                    drone.target_coord = hubs[idx_h + 1].coord
                    drone.hub = hubs[idx_h + 1]

                    drone.coord = hubs[idx_h + 1].coord
                    hubs[idx_h].drones.pop(idx_d)
                    drone.conn_turns += 1

                conn.pass_drones += 1
                drone.moved = True
                next = False

                break
        return next, log

    def move_drones_conns(
            self,
            drone: Drones
    ) -> list[str]:
        log = []
        # print("-----------------")

        conn = drone.conn

        hub_end = [
            _ for _ in self.confs.hubs if _.hub_name == drone.conn.end
        ]
        # print(f"hubs: {[_.hub_name for _ in hub_end]}")

        hub_end = hub_end[0]
        if len(hub_end.drones) == hub_end.max_drones:
            raise ("shit in max drones. Need another protection")
        drone.start_coord = drone.target_coord
        drone.target_coord = hub_end.coord
        hub_end.drones.append(drone)
        conn.drones.pop(conn.drones.index(drone))
        conn.pass_drones = len(conn.drones)
        drone.conn = None
        # print()
        return log

    def walk_one(
            self,
            drones: list[Drones],
            type: str = 'hub'
    ) -> list[str]:

        log = []
        paths = self.sorted_paths

        for drone in drones:
            if type == 'connection':
                # pass
                log.extend(self.move_drones_conns(drone))
            else:
                next = True
                for path in paths:
                    # if next is False:
                    #     break

                    if len(drones) == 0:
                        break

                    # validate drones in hubs
                    if type == 'hub':
                        next, this_log = self.move_drones_hubs(
                            drone, path.hubs, next
                        )
                    log.extend(this_log)

        return log

    def find_drones_h(self) -> list[Drones]:
        drones = []
        for hub in self.confs.hubs:
            for drone in hub.drones:
                drone.moved = False
                drones.append(drone)

        drones = [
            drone for drone in sorted(drones, key=lambda x: x.id)
            if drone.finished is False
        ]
        return drones

    def find_drones_c(self) -> list[Drones]:
        drones = []
        for conn in self.confs.all_connections:
            conn.pass_drones = len([
                _ for _ in conn.drones
                if _.conn_wait == 2
            ])
            for drone in conn.drones:
                drone.moved = False
                drone.conn_wait -= 1
                drones.append(drone)

        drones = [
            drone for drone in sorted(drones, key=lambda x: x.id)
            if drone.finished is False and drone.conn_wait == 0
        ]
        return drones

    def find_after_conn(self) -> list[Drones]:
        drones = []
        for conn in self.confs.all_connections:
            for drone in conn.drones:
                drone.moved = False
                if drone.conn_wait < 0:
                    raise "Shit happened here"

                hubs = list(
                    filter(lambda x: x.hub_name == conn.end, self.confs.hubs)
                )
                drones.extend([_.drones for _ in hubs])

        return drones

    def reset_moving(self):
        for drone in self.confs.all_drones:
            drone.moving = True
            drone.progress = 0

    def walk(self) -> None:
        log = []

        self.reset_moving()
        self.hubs_w_drones = self.f_hubs_w_drones()
        drones_after_conns = self.find_after_conn()
        if len(drones_after_conns) != 0:
            log.extend(self.walk_one(drones_after_conns))

        drones_conns = self.find_drones_c()
        if len(drones_conns) != 0:
            self.walk_one(drones_conns, type='connection')

        drones_hubs = self.find_drones_h()
        drones_hubs = list(
            filter(lambda x: x not in drones_conns, drones_hubs)
        )
        if len(drones_hubs) != 0:
            log.extend(self.walk_one(drones_hubs))
        if len(log):
            print(" ".join(log))
        return None
