from .exceptions import ConfsError
from .drones import Drones


class ConnectionNodes:
    """
    Class that has all the connection nodes
    """
    def __init__(
        self,
        path: str,
        confs: str | None
    ):
        """
        initiates the class
        Args:
            path (str): the path (start and end hub)
            confs (str): metadata (if any)
        """
        self.path: str = path
        self.confs: str | None = confs
        self.start: str = ""
        self.end: str = ""
        self.pass_drones = 0
        self.max_drones: int = 1
        self.drones: list[Drones] = []
        self.split_path()
        self.coord: tuple[float, float]
        self.extract_confs()

    def split_path(self) -> None:
        """
        Splits path into start and end huv
        """
        conn = self.path.split('-')
        if self.path is None or len(conn) != 2:
            raise ValueError("Connection must have exactly one '-'")
        self.start = conn[0]
        self.end = conn[1]
        return None

    def extract_confs(self) -> None:
        """
        extracts max_link_capacity from metadata
        ensures no more metada is available
        """
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
            self.max_drones = max_link
        except Exception:
            raise ConfsError(f"{confs[1]} is not numeric")
        if max_link < 0:
            raise ConfsError(
                f"max_link_capacity must be > 0 and is {max_link}"
            )
        # return max_link
        return None
