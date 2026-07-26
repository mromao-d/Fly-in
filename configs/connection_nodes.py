from exceptions import ConfsError
from drones import Drones


class ConnectionNodes:
    def __init__(
        self,
        path: str,
        confs: str | None
    ):
        self.path: str = path
        self.confs: str = confs
        self.start: str = None
        self.end: str = None
        self.pass_drones = 0
        self.max_drones: int = 1
        self.drones: list[Drones] = []
        self.split_path()
        self.coord: tuple[int, int] = tuple()
        self.extract_confs()

    def split_path(self):
        conn = self.path.split('-')
        if self.path is None or len(conn) != 2:
            raise ValueError("Connection must have exactly one '-'")
        self.start = conn[0]
        self.end = conn[1]

    def extract_confs(self) -> None:
        if self.confs is None:
            return None
        confs = self.confs.split(' ')
        if len(confs) != 1:
            raise ConfsError("Only one parameter accepted")
        confs = confs[0].split('=')
        if confs[0].lower() != 'max_link_capacity':
            raise ConfsError(f"Wrong metadata {confs[0]}")
        try:
            max_link = int(confs[1])
            if max_link < 0:
                raise ConfsError("max_link_capacity must be > 0")
            self.max_drones = max_link
        except ConfsError:
            raise (f"{confs[1]} is not numeric")
        return max_link
