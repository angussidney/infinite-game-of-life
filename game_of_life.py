alive_cells = set()


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


def get_no_alive_neighbours(cell):
    """
    Find how many 'alive' cells are neighbouring a certain cell
    :param cell: An (x, y) tuple representing the coordinates of a particular cell
    :return: The number of adjacent cells which are alive
    """
    alive = 0
    for neighbour in get_neighbours(cell):
        if neighbour in alive_cells:
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
    for cell in alive_cells:
        relevant += get_neighbours(alive)
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
        if cell not in world_state and get_no_alive_neighbours(cell) == 3:
            new_world_state.add(cell)
        elif cell in world_state and get_no_alive_neighbours(cell) in [2, 3]:
            new_world_state.add(cell)
