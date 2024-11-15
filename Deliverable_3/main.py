import path_gen as pg
import path_find as pf

"""
    Generate the world with paths and voids

    Generating options:
    - Random world generator
    - Slightly smarter world generator

"""

world = pg.random_world()
# pg.see(world, "Random 16x16 World")

# world = pg.smarter_world(4, 50)
# pg.see(world, "Smarter 16x16 World")

# pg.see(world)


""" 
    Find the shortest path using A* search

    Options for selecting the points:
    - Two random points
    - Random points from either edges of the world
    - Enter your own points manually
    - Pick the points on the map

"""

# start, finish = pf.find_random_cells(world)
# start, finish = pf.find_most_distant(world)
# start, finish = pf.enter_own_points(world)
start, finish = pf.find_own_points(world)

path = pf.a_star_search(world, start, finish)


""" 
    Plot the Generated world and the shortest path
    (if available)

"""

pf.plot_path(world, path)

"""
    Block a path tile and make it background

"""

while(path is not None):
    world = pg.block_path(world)

    path = pf.a_star_search(world, start, finish)

    pf.plot_path(world, path)
