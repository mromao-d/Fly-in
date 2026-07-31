from render import RenderMap
from read_confs import ReadConfs
from algo import Algo
import traceback

# duvidas:
## caso o caralho do drones demore 2 turnos a chegar, o caralho do caminho pode ser usado por outro drone quando o caralho do 1º drone é entre à porra do hub?

if __name__ == '__main__':
    try:
        file1 = './maps/easy/02_simple_fork.txt'
        medium1 = './maps/medium/01_dead_end_trap.txt'
        medium2 = './maps/medium/02_circular_loop.txt'
        medium3 = './maps/medium/03_priority_puzzle.txt'
        hard3 = './maps/hard/03_ultimate_challenge.txt'
        file4 = './maps/challenger/01_the_impossible_dream.txt'
        confs = ReadConfs(medium3)
        # for con in confs.all_connections:
        #     print(f"{con.start} with confs: {confs}")
        di = Algo(confs)
        # for conn in di.confs.all_connections:
        #     print(f"conn {conn.path} has capacity of {conn.max_link_capacity} with max_drones = {conn.max_drones}")
        # drones = di.find_drones()
        # di.walk_one(drones)
        # drones = di.find_drones()
        # di.walk_one(drones)
        # di.walk()
        map = RenderMap(confs)
    except Exception as e:
        print(f"ERROR || {e}")
        traceback.print_exc()
