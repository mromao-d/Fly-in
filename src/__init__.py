from .render import RenderMap
from .read_confs import ReadConfs
from .algo import Algo
import traceback


def run(file: str):
    try:
        confs = ReadConfs(file)
        Algo(confs)
        RenderMap(confs)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        last = tb[-1]
        print(f"ERROR || {e} on file {last.filename}, row {last.lineno}")
