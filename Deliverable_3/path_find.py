# Python program for A* Search Algorithm
import math
import heapq

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import random

# Define the Cell class


class Cell:
    def __init__(self):
      # Parent cell's row index
        self.parent_i = 0
    # Parent cell's column index
        self.parent_j = 0
    # Total cost of the cell (g + h)
        self.f = float('inf')
    # Cost from start to this cell
        self.g = float('inf')
    # Heuristic cost from this cell to destination
        self.h = 0


# Define the size of the grid
ROW = 16
COL = 16

# Check if a cell is valid (within the grid)


def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked


def is_unblocked(grid, row, col):
    return grid[row][col] == 1

# Check if a cell is the destination


def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Trace the path from source to destination


def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]

    while not (cell_details[row, col].parent_i == row and cell_details[row, col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row, col].parent_i
        temp_col = cell_details[row, col].parent_j
        row = temp_row
        col = temp_col

    path.append((row, col))
    path.reverse()

    return path

"""
 Finds the random two cells and 
 sets them as start and finish
"""
def find_random_cells(grid):
    start = [random.randint(0, 15), random.randint(0, 15)]
    while True:
        if grid[tuple(start)] == 1:
            break
        else:
            start = [random.randint(0, 15), random.randint(0, 15)]

    finish = [random.randint(0, 15), random.randint(0, 15)]
    while True:
        if grid[tuple(finish)] == 1:
            break
        else:
            finish = [random.randint(0, 15), random.randint(0, 15)]

    return (tuple(start), tuple(finish))

"""
 Find the two most distant points on the grid
"""
def find_most_distant(grid):
    start = [random.randint(0, 15), 0]
    while True:
        if grid[tuple(start)] == 1:
            break
        else:
            start = [random.randint(0, 15), 0]

    finish = [random.randint(0, 15), 15]
    while True:
        if grid[tuple(finish)] == 1:
            break
        else:
            finish = [random.randint(0, 15), 15]

    return (tuple(start), tuple(finish))

"""
 Enter your own points in the terminal
"""
def enter_own_points(grid):
    start = input("Please enter the start point in the shape: (x,y)\n")
    finish = input("Please enter the finish point in the shape: (x,y)\n")

    start = tuple(map(int, start.strip("()").split(",")))
    finish = tuple(map(int, finish.strip("()").split(",")))

    return (tuple(start), tuple(finish))

"""
 Click on the two points 
 First one will be the start
 Second will be the finish
"""
def find_own_points(grid):
    plt.imshow(grid, cmap="binary_r") 
    plt.xticks([]) 
    plt.yticks([]) 
    plt.title("Tap on your own points")

    clicks = []

    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            y = round(event.xdata)
            x = round(event.ydata)
            clicks.append((x, y))
            print(f'You clicked at coordinates: ({x}, {y})')
            if len(clicks) == 2:
                print("Two clicks received. Disconnecting the event handler.")
                plt.gcf().canvas.mpl_disconnect(cid)
                plt.close()  # Close the plot window after two clicks

    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    return (tuple(clicks[0]), tuple(clicks[1]))

# Implement the A* search algorithm

def a_star_search(grid, src, dest):
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return None

    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return None

    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return None

    closed_list = np.zeros((ROW, COL), dtype=bool)
    cell_details = np.array([[Cell() for _ in range(COL)] for _ in range(ROW)])

    i, j = src
    cell_details[i, j].f = 0
    cell_details[i, j].g = 0
    cell_details[i, j].h = 0
    cell_details[i, j].parent_i = i
    cell_details[i, j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    found_dest = False

    while len(open_list) > 0:
        p = heapq.heappop(open_list)
        i, j = p[1], p[2]
        closed_list[i, j] = True

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]

            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i, new_j]:
                if is_destination(new_i, new_j, dest):
                    cell_details[new_i, new_j].parent_i = i
                    cell_details[new_i, new_j].parent_j = j
                    print("The destination cell is found")
                    return trace_path(cell_details, dest)
                else:
                    g_new = cell_details[i, j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    if cell_details[new_i, new_j].f == float('inf') or cell_details[new_i, new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        cell_details[new_i, new_j].f = f_new
                        cell_details[new_i, new_j].g = g_new
                        cell_details[new_i, new_j].h = h_new
                        cell_details[new_i, new_j].parent_i = i
                        cell_details[new_i, new_j].parent_j = j

    print("Failed to find the destination cell")
    return None

"""
 Plot the path on the given grid
 Closes on-click
"""
def plot_path(grid, path, num=0):

    # Without this big the whole grid turns 
    # black and red when there is no blocked path
    if not np.any(grid == 2):
        cmap = mcolors.ListedColormap(['black', 'white'])
    else:
        cmap = mcolors.ListedColormap(['black', 'white', 'red'])

    plt.imshow(grid, cmap=cmap) 

    if path:
        path = np.array(path)
        plt.plot(path[:, 1], path[:, 0], marker='*', color='r')

    def onclick(event):
        plt.close()

    plt.gcf().canvas.mpl_connect('button_press_event', onclick)

    plt.savefig(f"./figures/Path{num}.png")

    plt.show()
