from read_confs import ReadConfs
from hubs import HubNodes


class Dinic:
    def __init__(self, confs: ReadConfs):
        """
        Inits the graph class
        Args:
            V: int = #Hubs (or #vertices)

        inits:
            adj: list[list[Edges]] = list adj hubs
            level: int = level of the node
        """
        self.confs = confs
        self.finish = False
        self.BFS()
        self.hub_validations()
        self.DFS()

    def find_start(self) -> HubNodes | None:
        start = next(
            (
                hub for hub in self.confs.hubs
                if hub.hub_type.value == 'start_hub'
            ),
            None
        )
        return start

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

    def DFS(self) -> None:
        start = self.find_start()
        if start is None:
            return None
        path = [start]
        visited = set()
        visited.add(start)
        end = False
        while path and end is False:
            hub = path[-1]
            if len(hub.conn_nodes) == 0:
                path.pop()
            elif all(x in visited for x in hub.conn_nodes):
                path.pop()
            else:
                for adj in sorted(hub.conn_nodes, key = lambda x: x.zone.value):
                    if (adj in visited or adj.zone.name == 'blocked'):
                        continue
                    
                    # elif adj.level >= hub.level:

                    elif adj.hub_type.value == 'end_hub':
                        path.append(adj)
                        end = True
                        break

                    else:
                        path.append(adj)
                        visited.add(adj)
                        break

        bottle = min([hub.max_drones for hub in path])
        # sorted_path = sorted(path, key = lambda x: x.zone.value)
        print(f"path is {[(hub.hub_name, hub.zone.value) for hub in path]} for {str(bottle)} drones")
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
