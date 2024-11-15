import matplotlib.pyplot as plt
import numpy as np
import random

ROW = 16
COL = 16

def random_world() -> np.ndarray:
    world = np.random.randint(2, size=(ROW, COL))
    return world

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

def block_path(world):
    plt.imshow(world, cmap="binary_r") 
    plt.xticks([]) 
    plt.yticks([]) 
    plt.title("Block some path")

    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            y = round(event.xdata)
            x = round(event.ydata)


        if(world[x,y] == 1):
            world[x,y] = 0
            plt.close()

    plt.gcf().canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    return world




def see(world: np.ndarray, name: str = "World"):
    plt.imshow(world, cmap="binary_r") 
    plt.xticks([]) 
    plt.yticks([]) 
    plt.title(name)
    plt.show() 
