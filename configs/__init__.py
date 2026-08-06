from render import RenderMap
from read_confs import ReadConfs
from algo import Algo
import traceback


if __name__ == '__main__':
    try:
        file1 = './maps/easy/02_simple_fork.txt'
        medium1 = './maps/medium/01_dead_end_trap.txt'
        medium2 = './maps/medium/02_circular_loop.txt'
        medium3 = './maps/medium/03_priority_puzzle.txt'
        hard3 = './maps/hard/03_ultimate_challenge.txt'
        file4 = './maps/challenger/01_the_impossible_dream.txt'
        confs = ReadConfs(hard3)
        di = Algo(confs)
        map = RenderMap(confs)
    except Exception as e:
        print(f"ERROR || {e}")
        # traceback.print_exc()
