from render import RenderMap
from read_confs import ReadConfs
from dinic import Dinic


if __name__ == '__main__':
    try:
        file1 = './maps/easy/01_linear_path.txt'
        file2 = './maps/medium/03_priority_puzzle.txt'
        file3 = './maps/hard/03_ultimate_challenge.txt'
        file4 = './maps/challenger/01_the_impossible_dream.txt'
        confs = ReadConfs(file3)
        Dinic(confs)
        # for hub in confs.hubs:
        #     print(f"hub {hub.hub_name} level is {hub.level}")
        map = RenderMap(confs)
    except Exception as e:
        print(f"ERROR || {e}")
