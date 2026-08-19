from .read_confs import ReadConfs
from .hubs import HubNodes, ZoneType, HubType
from .paths import Paths
from .drones import Drones
from typing import Any


class Algo:
    def __init__(self, confs: ReadConfs):
        """
        Inits the graph class
        Args:
            V: confs = Configurations

        """
        self.all_paths: list[Paths] = []
        self.confs = confs
        self.finish = False
        self.simulation_turns = 0
        self.graph: dict[HubNodes, list[HubNodes]] = {}
        self.BFS()
        self.hub_validations()
        self.build_graph()
        self.hubs_w_drones = self.f_hubs_w_drones()
        self.sorted_paths = self.ordered_paths()

    def find_start(self) -> HubNodes | None:
        """
        finds first node of the graph (start node)

        :param self: Description
        """
        start = next(
            (
                hub for hub in self.confs.hubs
                if hub.hub_type.value == 'start_hub'
            ),
            None
        )
        return start

    def find_end(self) -> HubNodes | None:
        """
        finds last node of the graph (end node)
        """
        end = next(
            (
                hub for hub in self.confs.hubs
                if hub.hub_type.value == 'end_hub'
            ),
            None
        )
        return end

    def BFS(self) -> None:
        """
        Used to validate if map has path between start and end
        can be deprecated
        """
        start = self.find_start()
        if start:
            q = [start]
            visited = {start}
            start.level = 0

            while q:
                hub = q.pop(0)

                for adj in hub.conn_nodes:
                    if adj in visited or adj.zone.name == 'blocked':
                        continue

                    if adj.hub_type.value == 'end_hub':
                        self.finish = True

                    adj.level = hub.level + 1

                    visited.add(adj)
                    q.append(adj)

        return None

    def build_graph(self) -> None:
        """
        builds the graph with the format:
        {
            hub: [con_hub1, con_hub2],
            ...
        }
        used to find all paths
        """
        for node in self.confs.hubs:
            self.graph[node] = node.conn_nodes

        return None

    @staticmethod
    def is_priority(path: list[HubNodes]) -> bool:
        """
        validates if all the choices on the path follow the
        priority rule

        Args:
            path(Paths): The path (list of hubs)

        returns:
            bool -> true if yes else no
        """
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
    def is_restricted(path: list[HubNodes]) -> bool:
        """
        validates if any choice is restricted
        think it can be deprecated

        Args:
            path(Paths): The path (list of hubs)

        returns:
            bool -> true if yes else no
        """
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

    def find_all_paths(self, hub: HubNodes | None) -> None:
        """
        finds all paths between start node and end node
        Args:
            hub (HubNodes): now is always start node.
            previous version accpted any node.
        """
        # if hub is None:
        #     return

        def find_path(
            node: Any,
            start: Any,
            end: Any,
            visited: Any = None
        ) -> Any:
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
                or node.zone == ZoneType.blocked
            ):
                return []

            visited = visited | {node}

            if node == end:
                return [[node]]

            paths = []
            for adj_node in self.graph.get(node, []):
                for path in find_path(adj_node, start, end, visited):
                    paths.append([node] + path)

            return paths

        start = hub
        end = self.find_end()
        paths = find_path(start, start, end)
        for p in paths:
            self.all_paths.append(Paths(
                hubs=p,
                priority=self.is_priority(p),
                restricted=self.is_restricted(p)
            ))
        return None

    def hub_validations(self) -> None:
        """
        - validates that map is linked between start and end
        - validates that no names are duplicated
        """
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
        """
        orders path by:
            - priority
            - cost
        returns:
            sorted_paths(list[Paths]): paths sorted by
                priority and cost
        """

        self.find_all_paths(self.find_start())

        sorted_paths = sorted(
            self.all_paths, key=lambda x: x.priority, reverse=True
        )
        sorted_paths = sorted(
            sorted_paths, key=lambda x: x.cost
        )

        return sorted_paths

    def f_hubs_w_drones(self) -> list[HubNodes]:
        """
        finds all hubs that have drones in them
        returns:
            list[HubNodes]: list of hubs that have drones
        """
        for hub in self.confs.hubs:
            for drone in hub.drones:
                drone.moved = False
        hubs_w_drones = list(
            filter(lambda x: len(x.drones) > 0, self.confs.hubs)
        )
        hubs_w_drones = [
            hub for hub in hubs_w_drones
            if hub.hub_type != HubType.end_hub
        ]
        return hubs_w_drones

    def move_drones_hubs(
            self,
            drone: Drones,
            hubs: list[HubNodes],
            next: bool
    ) -> tuple[bool, list[str]]:
        """
        Moves a drone from one hub to the next location in its path.

        Determines whether the drone can move based on hub capacity,
        connection availability, and restricted zone rules. The drone is
        either transferred to the next hub or placed on the connection
        leading to it.

        Args:
            drone (Drones): Drone to move.
            hubs (list[HubNodes]): Ordered list of hubs representing the
                drone's route.
            next (bool): Indicates whether the drone is allowed to move
                after previous path checks.

        Returns:
            tuple[bool, list[str]]:
                - Whether further movement is allowed in the current path.
                - Log messages generated by the movement.
        """
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
        """
        Moves a drone from the end of a connection to its destination hub.

        Updates the drone's coordinates, transfers it from the connection
        to the destination hub, updates the connection state, and clears
        the drone's active connection.

        Args:
            drone (Drones): Drone to move from a connection to a hub.

        Returns:
            list[str]: Log messages generated during the movement.
        """
        log: list[str] = []

        conn = drone.conn

        hubs_end = [
            _ for _ in self.confs.hubs
            if drone.conn and drone.conn.end and _.hub_name == drone.conn.end
        ]

        hub_end = hubs_end[0]
        if len(hub_end.drones) >= hub_end.max_drones:
            raise ValueError("shit in max drones. Need another protection")
        drone.start_coord = drone.target_coord
        drone.target_coord = hub_end.coord
        hub_end.drones.append(drone)
        if conn is not None:
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
        """
        Moves a group of drones during a simulation turn.

        Depending on the movement type, drones are either moved through
        connections or between hubs. Hub movements follow the configured
        sorted paths and generate movement logs.

        Args:
            drones (list[Drones]): Drones to move.
            type (str): Movement type. Use ``"connection"`` for drones
                travelling through connections or ``"hub"`` for drones
                moving between hubs.

        Returns:
            list[str]: Log messages describing the movements performed.
        """

        log = []
        paths = self.sorted_paths

        for drone in drones:
            if type == 'connection':
                # pass
                log.extend(self.move_drones_conns(drone))
            else:
                next = True
                for path in paths:

                    if len(drones) == 0:
                        break

                    if type == 'hub':
                        next, this_log = self.move_drones_hubs(
                            drone, path.hubs, next
                        )
                    log.extend(this_log)

        return log

    def find_drones_h(self) -> list[Drones]:
        """
        Finds active drones currently located at hubs.

        Retrieves drones from hubs ordered by descending hub level,
        resets their movement status, and excludes drones that have
        already completed their route.

        Returns:
            list[Drones]: Active drones currently waiting at hubs.
        """
        drones = []
        ordered_hubs = (
            sorted(self.confs.hubs, key=lambda x: x.level, reverse=True)
        )
        for hub in ordered_hubs:
            for drone in hub.drones:
                drone.moved = False
                drones.append(drone)

        drones = [
            drone for drone in drones
            if drone.finished is False
        ]
        return drones

    def find_drones_c(self) -> list[Drones]:
        """
        Finds drones currently travelling through connections.

        Updates the number of drones passing through each connection,
        decreases the remaining connection wait time for each drone,
        resets their movement status, and removes drones that have
        already completed their route.

        Returns:
            list[Drones]: Drones that are still active on connections,
            sorted by drone ID.
        """
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
            if drone.finished is False
        ]
        return drones

    def find_after_conn(self) -> list[Drones]:
        """
        Finds drones that have just completed traversing a connection.

        For each connection, resets the movement flag of its drones and
        collects the drones currently located at the destination hubs of
        those connections.

        Returns:
            list[Drones]: Drones at hubs reached from active connections.
        """
        drones: list[Drones] = []
        for conn in self.confs.all_connections:
            for drone in conn.drones:
                drone.moved = False
                if drone.conn_wait < 0:
                    raise ValueError("Shit happened here")

                hubs = list(
                    filter(lambda x: x.hub_name == conn.end, self.confs.hubs)
                )
                for hub in hubs:
                    drones.extend(hub.drones)

        return drones

    def reset_moving(self) -> None:
        """
        Resets the movement state of all drones for a new simulation turn.

        Marks every drone as ready to move and resets its movement progress
        along its current connection.
        """
        for drone in self.confs.all_drones:
            drone.moving = True
            drone.progress = 0

    def walk(self) -> tuple[int, int]:
        """
        Executes one simulation turn.

        The method:
            - resets drone movement state;
            - moves drones that have just exited a connection;
            - moves drones currently travelling through connections;
            - moves drones waiting at hubs;
            - logs and prints all hub movements.

        Returns:
            tuple[int, int]:
                - Total number of simulation turns elapsed.
                - Number of drones that moved during this turn.
        """
        log = []

        self.reset_moving()
        self.hubs_w_drones = self.f_hubs_w_drones()
        drones_after_conns = self.find_after_conn()
        if len(drones_after_conns) != 0:
            log.extend(self.walk_one(drones_after_conns))

        drones_conns = self.find_drones_c()
        drones_conns = list(
            filter(lambda x: x not in drones_after_conns, drones_conns)
        )
        if len(drones_conns) != 0:
            self.walk_one(drones_conns, type='connection')

        drones_hubs = self.find_drones_h()
        drones_hubs = list(
            filter(lambda x: x not in drones_conns, drones_hubs)
        )
        drones_hubs = list(
            filter(lambda x: x not in drones_after_conns, drones_hubs)
        )
        if len(drones_hubs) != 0:
            log.extend(self.walk_one(drones_hubs))
        if len(log):
            print(" ".join(log))
            self.simulation_turns += 1
        return self.simulation_turns, len(log) + len(drones_conns)
