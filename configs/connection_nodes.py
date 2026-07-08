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
        conn = self.path.split('-')
        if self.path is None or len(conn) != 2:
            raise ValueError("Connection must have exactly one '-'")
        self.start = conn[0]
        self.end = conn[1]
