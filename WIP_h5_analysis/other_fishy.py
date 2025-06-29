import h5py as h5
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# dummy data to test animations
x = [0, 1, 2, 3, 4]
y = [0, 1, 2, 3, 4]

# global variables
fig, ax = plt.subplots()
fly = "courtship_labels.000_20190128_113421.analysis.h5"
meece = "micepractice.000_mice.analysis.h5"
other_fishy = 'fishyanalysis.h5'

# things I can refactor, I think.
stuff = {}

def init_func():
    print(f"hello")
    plot_line(0)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_title(f"hello")

def plot_line(frame):
    ax.clear()
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_title(f"frame: {frame}")
    ax.plot(x[:frame+1], y[:frame+1])

# find all edges and make sure there are no duplicates.
def find_edges(filename):
    edges = set()
    for node1, node2 in filename['edge_names']:
        # decode the byte strings and sort the edges.
        # sorted expects an iterable, so create a list
        # returns a list
        s = sorted({node1.decode('utf-8'), node2.decode('utf-8')})
        
        # convert to tuple because sets cannot store lists
        t = tuple(s)
    
        # add tuple to set. Should automatically fail silently if a duplicate edge is added.
        edges.add(t)
    return edges

# plot edges for a skeleton, given a dictionary of their names as keys and coordinates as values.
def plot_edges(instance, frame, edges, axes, filename):
    
    x_coords = filename['tracks'][instance, 0, :, frame]
    y_coords = filename['tracks'][instance, 0, :, frame]
    print(edges)
    return

    # TODO: delete after I figure out how to plot edges directly from ['tracks']
    # for node1, node2 in edges:
    #     x = (node_coords[node1][0], node_coords[node2][0])
    #     y = (node_coords[node1][1], node_coords[node2][1])
    #     axes.plot(x, y)

def plot_frame(frame, filename):
    
    ax.clear()
    ax.set_title(f"frame: {frame}")

    # find edges.
    edges = find_edges(filename)

    # node names are stored as byte strings, decode them.
    node_names = []
    
    for node in filename['node_names']:
        node = node.decode('utf-8')
        node_names.append(node)

    # store coordinates for each node, so we can later draw edges.
    node_coords = {}

    # The shape of the tracks dataset is 4-dimensional numpy array where:
    # The first index of tracks signifies animal instances.
    # The second index: x(0) or y(1) coordinates
    # The third: Body parts, in order listed by filename['node_names']
    # The fourth: The frame number of the video
    # When looping over numpy arrays, each loop will iterate over the first index.
    # In other words, loop over each animal instance.
    for i, instance in enumerate(filename['tracks']):
        
        print(f"animal: {i}")

        # For each instance, grab their x and y coordinates for every body part on this particular frame.
        x_coordinates = instance[0, :, frame]
        y_coordinates = instance[1, :, frame]
    
        # pair the coordinates together, so we can loop over them.
        coords = zip(x_coordinates, y_coordinates)

        # Loop over every pair of x and y coordinates
        for j, (x_coord, y_coord) in enumerate(coords):

            node = node_names[j]

            # plot each coordinate as a point, using the 'o' argument.
            ax.plot(x_coord, y_coord, 'o')

            # label each point using data from the 'node_names' dataset.
            ax.text(x_coord, y_coord, node)

            '''
            I technically shouldn't need to do this, I think.
            each fish's x/y coordinates are stored in ['tracks']
            try to grab from that, instead of storing it here
            '''
            # # store coordinates for this node.
            # if node not in node_coords:
            #     node_coords[node] = (x_coord, y_coord)

            # else:
            #     raise Exception(f"duplicate node: {node}? what do? exit and start debugging!")
        # plot edges
        plot_edges(i, frame, edges, ax, filename)
                    

def visible_frames(filename):
    v = []
    # each row is an array of binary flags (0/1) on whether a given instance was detected or not.
    for i, row in enumerate(filename['track_occupancy']):
        if np.any(row) > 0:
            v.append(i)
    return v

# takes an iterable (hopefully) of frames to animate.
def animate_frames(frames, filename):
    # FuncAnimation requires its second argument to be a function with one parameter.
    # Since plot_frame requires 2, create a partial function to implicitly call the 2nd argument.
    p = partial(plot_frame, filename=filename)

    # FuncAnimation started an event loop by calling matplotlib.animation.TimedAnimation()
    # The animation will run so long as a reference to it is kept alive, so return it.
    return animation.FuncAnimation(fig, p, frames=frames, interval=1000)

if __name__ == "__main__":
    try:
        with h5.File(other_fishy, 'r') as f:
            v = visible_frames(f)
            find_edges()
            plot_frame(v[0], f)
            plt.show()
            
    except Exception as e:
        print(f"no idea what to do with exceptions, so I'll just print them out for now: \n\te: {e}")
