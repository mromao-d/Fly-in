from read_confs import ReadConfs


class Dinic:
    def __init__(self, confs: ReadConfs):
        """
        Inits the graph class
        Args:
            V: int = #Hubs (or #vertices)

        inits:
            adj: list[list[Edges]] = list adjacent hubs
            level: int = level of the node
        """
        self.confs = confs
        self.finish = False
        self.BFS()
        self.hub_validations()

    def BFS(self):
        start = next(
            (
                hub for hub in self.confs.hubs
                if hub.hub_type.value == 'start_hub'
            ),
            None
        )
        if start:
            q = [start]
            visited = set()
            print(start.hub_name)
            start.level = 0
            q.append(start)

            while q:
                hub = q.pop(0)

                for adjacent in hub.conn_nodes:
                    if adjacent in visited or adjacent.zone.name == 'blocked':
                        continue

                    if adjacent.hub_type.value == 'end_hub':
                        self.finish = True

                    adjacent.level = hub.level + 1

                    q.append(adjacent)
                    visited.add(adjacent)

    def hub_validations(self):
        if self.finish is False:
            raise Exception("Map is linked between start and end")
        for hub in self.confs.hubs:
            hubs = list(
                filter(lambda x: x.hub_name == hub.hub_name, self.confs.hubs)
            )
            if len(hubs) > 1:
                raise Exception(f"More than one hub called {hub.hub_name}")
