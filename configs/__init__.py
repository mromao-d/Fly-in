from render import RenderMap
from read_confs import ReadConfs
from algo import Algo


if __name__ == '__main__':
    try:
        file1 = './maps/easy/02_simple_fork.txt'
        file2 = './maps/medium/03_priority_puzzle.txt'
        file3 = './maps/hard/03_ultimate_challenge.txt'
        file4 = './maps/challenger/01_the_impossible_dream.txt'
        confs = ReadConfs(file2)
        di = Algo(confs)
        paths = di.all_paths
        # print(f"paths are {paths}")
        # print(f"paths are {[path.priority for path in paths]}")
        # for path in paths:
        #     print(f"{[_.hub_name for _ in path.path]} with cost {path.cost}")
        #     print([_.path for _ in path])
        map = RenderMap(confs)
        di.walk()
    except Exception as e:
        print(f"ERROR || {e}")
