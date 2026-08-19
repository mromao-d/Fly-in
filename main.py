if __name__ == '__main__':
    # import sys

    """
    run program
    """
    from sys import argv
    import src

    file1 = 'maps/easy/02_simple_fork.txt'
    medium1 = 'maps/medium/01_dead_end_trap.txt'
    medium2 = 'maps/medium/02_circular_loop.txt'
    medium3 = 'maps/medium/03_priority_puzzle.txt'
    hard3 = 'maps/hard/03_ultimate_challenge.txt'
    file4 = 'maps/challenger/01_the_impossible_dream.txt'

    if len(argv) == 1:
        src.run(hard3)

    else:
        src.run(argv[1])
