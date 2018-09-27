from math import inf


"""
      ^ y+
      |
x- <--+--> x+
      |
      V y-
"""


def get_neighbours(cell):
    """
    Returns the coordinates of the neighbours to a particular cell
    :param cell: An (x, y) tuple representing the coordinates of a particular cell
    :return: A set containing all adjacent cell coordinates
    """
    neighbours = set()
    for x_mod in [-1, 0, 1]:
        for y_mod in [-1, 0, 1]:
            if x_mod == 0 and y_mod == 0:
                continue  # We don't want to count this cell as a neighbour
            else:
                cell_coords = (cell[0] + x_mod, cell[1] + y_mod)
                neighbours.add(cell_coords)
    return neighbours


def get_no_alive_neighbours(cell, world_state):
    """
    Find how many 'alive' cells are neighbouring a certain cell
    :param cell: An (x, y) tuple representing the coordinates of a particular cell
    :param world_state: All of the currently alive cells
    :return: The number of adjacent cells which are alive
    """
    alive = 0
    for neighbour in get_neighbours(cell):
        if neighbour in world_state:
            alive += 1
    return alive


def get_all_relevant_dead_cells(alive):
    """
    Find all dead cells which are neighbouring an alive cell
    These will need to be considered for the next generation
    :param alive: All of the currently alive cells
    :return: A set containing all relevant cell coordinates
    """
    relevant = set()
    for cell in alive:
        relevant.update(get_neighbours(cell))
    relevant -= alive  # We only want dead cells
    return relevant


def next_world_state(world_state):
    """
    Computes the next world state
    :param world_state: Current world state (set of alive cell coordinates)
    :return: New world state (set of alive cell coordinates)
    """
    new_world_state = set()
    for cell in get_all_relevant_dead_cells(world_state):
        if get_no_alive_neighbours(cell, world_state) == 3:
            new_world_state.add(cell)
    for cell in world_state:
        if get_no_alive_neighbours(cell, world_state) in [2, 3]:
            new_world_state.add(cell)
    return new_world_state


def represent_world(world_state, x1, y1, x2, y2, alive="██", dead="  ", fill=""):
    """
    Creates an ASCII art image representing the world bounded by the given coordinates
    :param world_state: Current world state (set of alive cell coordinates)
    :param x1: First column to be displayed
    :param y1: First row to be displayed
    :param x2: Stop column (i.e. x1 <= x < x2 will be displayed)
    :param y2: Stop row to be displayed (i.e. y1 <= y < y2 will be displayed)
    :param alive: Character to be displayed for alive cells
    :param dead: Character to be displayed for dead cells
    :param fill: Character to be displayed to horizontally pad each cell
    :return: String representing world within those coordinates (bordered by hashes)
    """
    lines = []
    for y in reversed(range(y1, y2)):
        lines.append("#" + fill.join([alive if (x, y) in world_state else dead for x in range(x1, x2)]) + "#")
    return "#" * len(lines[0]) + "\n" + "\n".join(lines) + "\n" + "#" * len(lines[0])


def evolve_world(initial_state, generations):
    """
    Evolves the world over the given number of generations, returning a list of all generations
    :param initial_state: Initial world state (set of alive cell coordinates)
    :param generations: Number of times the world should be evolved
    :return: A list of world states for each generation, including initial state
    """
    world_states = [initial_state]
    for _ in range(generations):
        world_states.append(next_world_state(world_states[-1]))
    return world_states


def generate_file(x, y, filename="world.txt"):
    """
    Generates an x*y grid of dots (i.e. empty world state) in a file
    :param x: Width of grid
    :param y: Height of grid
    :param filename: Name for file to be created (defaults to world.txt)
    """
    with open(filename, "w+") as f:
        for _ in range(y):
            f.write(("." * x) + "\n")


def import_file(filename="world.txt", alive_char="@"):
    """
    Imports a world state from the given file. Active cells will be centered over (0, 0)
    :param filename: Name of file to import from
    :param alive_char: The character which has been used to represent an alive cell
    :return: World state - a set of alive cell coordinates
    """
    alive = set()
    # Set min and max as infinity and -infinity so that anything < min == true
    x_min, y_min = inf, inf
    x_max, y_max = -inf, -inf
    with open(filename, "r") as f:
        for y, line in enumerate(l.strip() for l in f):
            for x, char in enumerate(line):
                if char == alive_char:
                    # Update the current bounding box for all live cells
                    if x < x_min:
                        x_min = x
                    elif x > x_max:
                        x_max = x
                    if y < y_min:
                        y_min = y
                    elif y > y_max:
                        y_max = y
                    alive.add((x, -y))
    x_offset = (x_max - x_min) // 2
    y_offset = (y_max - y_min) // 2
    # This goes through each alive cell and offsets it such that they are roughly centered over (0, 0)
    offset_alive = {(x - x_offset - x_min, y - y_offset + y_max) for x, y in alive}
    return offset_alive


def main():
    from time import sleep

    if input("Type anything to generate new pattern (else press enter): "):
        x = int(input("Width: "))
        y = int(input("Height: "))
        generate_file(x, y)
        input("Press enter once file is filled out...")
    alive_cells = import_file()
    x1 = int(input("x1: "))
    x2 = int(input("x2: "))
    y1 = int(input("y1: "))
    y2 = int(input("y2: "))
    gens = int(input("generations: "))
    states = evolve_world(alive_cells, gens)

    for state in states:
        print("\033[;H\033[2J")
        print(represent_world(state, x1, y1, x2, y2))
        sleep(0.5)


if __name__ == "__main__":
    main()
