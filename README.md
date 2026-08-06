*This project has been created as part of the 42 curriculum by mromao-s*

# Fly-in

## Description

Fly-in is a drone routing and pathfinding simulation. Given a directed graph defined in a plain-text map file, the program dispatches a fleet of drones from a start hub and routes them to an end hub as efficiently as possible, then renders the result as a real-time animated visualization.

The core problem is scheduling multiple drones through a capacity-constrained graph:

- Each **hub** (node) has a maximum number of drones it can hold simultaneously.
- Each **connection** (directed edge) has a maximum link capacity (drones that may traverse it per turn).
- Hubs can belong to different **zone types** that influence routing priority:
  - `normal` — standard hub
  - `priority` — preferred in path selection (lower cost)
  - `restricted` — drones take two turns to pass through (transit via connection object)
  - `blocked` — impassable

The algorithm (BFS + greedy path assignment) discovers all valid paths from start to end, ranks them by cost and priority, then steps every drone forward one hub per simulation turn while respecting all capacity constraints. The pygame renderer animates drones moving smoothly between hubs and displays live metrics (total path cost, drones moved, simulation turns).

### Project structure

```
Fly-in/
├── configs/
│   ├── __init__.py         # entry point
│   ├── algo.py             # BFS, path ranking, drone scheduling
│   ├── read_confs.py       # map file parser
│   ├── render.py           # pygame visualization
│   ├── hubs.py             # HubNodes, HubType, ZoneType
│   ├── drones.py           # Drone animation & state
│   ├── paths.py            # Path cost & bottleneck calculation
│   ├── connection_nodes.py # Connection (edge) parsing
│   └── exceptions.py       # Custom config errors
└── maps/
    ├── easy/               # 3 beginner maps
    ├── medium/             # 3 intermediate maps
    ├── hard/               # 3 advanced maps
    └── challenger/         # 1 extreme map
```

### Map file format

```
# comment
nb_drones: <N>

start_hub: <name> <x> <y> [color=<color>]
hub: <name> <x> <y> [color=<color> zone=<zone> max_drones=<N>]
end_hub: <name> <x> <y> [color=<color>]

connection: <start>-<end> [max_link_capacity=<N>]
```

Valid zone values: `normal`, `priority`, `restricted`, `blocked`.

## Instructions

### Prerequisites

- Python 3.12+
- pygame

```bash
pip install pygame
```

### Running

The entry point is `configs/__init__.py`. Run it from the **project root**:

```bash
cd configs
python __init__.py
```

To change the map being loaded, edit the `file1` / `hard3` / etc. variable at the bottom of `configs/__init__.py` and point it to the desired map path:

```python
confs = ReadConfs('./maps/easy/01_linear_path.txt')
```

### Controls

Close the pygame window to exit the simulation.

### Available maps

| Difficulty   | File                          | Drones | Description                        |
|--------------|-------------------------------|--------|------------------------------------|
| Easy         | `easy/01_linear_path.txt`     | 2      | Simple linear path                 |
| Easy         | `easy/02_simple_fork.txt`     | —      | Basic fork                         |
| Easy         | `easy/03_basic_capacity.txt`  | —      | Capacity constraint intro          |
| Medium       | `medium/01_dead_end_trap.txt` | —      | Dead-end traps                     |
| Medium       | `medium/02_circular_loop.txt` | —      | Circular loop                      |
| Medium       | `medium/03_priority_puzzle.txt`| —     | Priority zone puzzle               |
| Hard         | `hard/01_maze_nightmare.txt`  | 8      | Complex maze with dead ends        |
| Hard         | `hard/02_capacity_hell.txt`   | —      | Severe capacity constraints        |
| Hard         | `hard/03_ultimate_challenge.txt`| —    | Combined challenge                 |
| Challenger   | `challenger/01_the_impossible_dream.txt`| — | Extreme map                  |

## Resources

### Algorithms & graph theory

- [BFS (Breadth-First Search) — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Maximum flow problem — Wikipedia](https://en.wikipedia.org/wiki/Maximum_flow_problem)
- [Dinic's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dinic%27s_algorithm)
- [Graph theory fundamentals — Khan Academy](https://www.khanacademy.org/computing/computer-science/algorithms)

### Libraries

- [pygame documentation](https://www.pygame.org/docs/)
- [Python `enum` module](https://docs.python.org/3/library/enum.html)

### AI usage

Claude (claude.ai) was used to assist with:

- **Generating this README** — providing structure, section content, and the map format table based on the source code.
- **Debugging** — explaining error messages and suggesting fixes for edge cases in path validation and drone scheduling logic.
- **Code review** — reviewing the BFS and drone movement routines for correctness and suggesting cleaner iteration patterns.
