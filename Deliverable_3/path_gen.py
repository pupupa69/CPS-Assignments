import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import random

ROW = 16
COL = 16

"""
 Create a random grid with equal probability 
 of the cell being black or white
"""
def random_world() -> np.ndarray:
    world = np.random.randint(2, size=(ROW, COL))
    return world

"""
 Create a world with a few initial path cells that 
 make their neighbours on the right paths with 
 probability p
"""
def smarter_world(num_start_points: int, chance_of_path: int) -> np.ndarray:
    # Create a 16x16 grid filled with zeros

    world = np.zeros((ROW, COL), dtype=int)

    # Fill in the first random cells

    for point in range(num_start_points):
        start = random.randint(0,COL-1)
        world[start, 0] = 1

    # Fill next ones

    for j in range(1, COL):
        for i in range(ROW):
            if (i > 0 and world[i-1, j-1] == 1) or (world[i, j-1] == 1) or (i < ROW-1 and world[i+1, j-1] == 1):
                if(random.randint(0,100) <= (chance_of_path)):
                    world[i, j] = 1

    # See the world

    return world

"""
 Open the map of the world, and choose a cell to 
 become background
"""
def block_path(world, num=0):

    # Without this big the whole grid turns 
    # black and red when there is no blocked path
    if not np.any(world == 2):
        cmap = mcolors.ListedColormap(['black', 'white'])
    else:
        cmap = mcolors.ListedColormap(['black', 'white', 'red'])

    plt.imshow(world, cmap=cmap) 
    plt.xticks([]) 
    plt.yticks([]) 
    plt.title("Block some path")

    # On-click event
    # This will check if the clicked cell is white
    # and make it black if it was
    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            y = round(event.xdata)
            x = round(event.ydata)


        if(world[x,y] == 1):
            world[x,y] = 2      # Change to 0 if don't care about the colour
            plt.close()

    plt.gcf().canvas.mpl_connect('button_press_event', onclick)

    # plt.savefig(f"./figures/Blocked_path{num}.png")

    plt.show()

    return world

"""
 Plot the current world
"""
def see(world: np.ndarray, name: str = "World"):
    plt.imshow(world, cmap="binary_r") 
    plt.xticks([]) 
    plt.yticks([]) 
    plt.title(name)
    plt.savefig(f"./figures/{name}.png")

    def onclick(event):
        plt.close()

    plt.gcf().canvas.mpl_connect('button_press_event', onclick)

    plt.show() 

    
