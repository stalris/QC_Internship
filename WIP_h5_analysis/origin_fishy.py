# ihavenoideawhatimdoingdog.jpeg
import h5py as h5
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class SLEAP_Instance_Class:
    def __init__(self, filename):
        s = """
        print this object for a bad tutorial :) e.g.:
        fly = SLEAP_INSTANCE_CLASS('filename_here.h5')
        print(fly)

        """
        print(s)

        self.filename = filename
    
    # Stackoverflow and chatgpt says to use context manager protocols for handling files.
    def __enter__(self):

        # open a file and keep it open.
        self.file = h5.File(self.filename, 'r')

        # find the edges of this skeleton.
        self.edges = self.find_edges()

        # find the indices
        self.nodes = self.find_nodes()

        # Open a figure and axes, so we can plot the skeletons.
        self.fig, self.axes = plt.subplots()

        # Find all frames where there is at least one visible instance.
        self.v = self.visible_frames()
    
        # Think this returns the object, which is required from the context manager.
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception occured, of type: {exc_type}")
            print(f"\tvalue: {exc_value}")
            print(f"traceback: {traceback}")
        else:
            self.file.close()
    
    def __str__(self):
        s = """
        I designed this class to be used with the context manager protocol, so use it :)
        For context: that's the with/as block
        e.g. 
        with SLEAP_INSTANCE_CLASS('filename_here.h5') as whatever_file_variable_here:
            whatever_file_variable_here.print_datasets()
        You can even open multiple context managers at once! e.g.:
        with SLEAP_Instance_Class('file1.h5') as f, SLEAP_Instance_Class('file2.h5') as g:
            f.print_datasets()
            g.print_datasets()
        """
        return s 

    # I'll try to include some information for datasets here.
    def print_datasets(self):
        print(f"File: {self.file}")
        for dataset in self.file:
            print(f"\tdataset: {dataset}")

    def find_edges(self):

        # Store edges in a set to filter out duplicates.
        edges = set()

        for node1, node2 in self.file['edge_names']:

            # SLEAP stores edges as byte strings. Decode them.
            node1 = node1.decode('utf-8')
            node2 = node2.decode('utf-8')

            # sort the edges, returns a list.
            edge = sorted([node1, node2])

            # lists can't be stored in sets, so convert to a tuple first.
            t = tuple(edge)

            # store in edges. Duplicates will fail silently.
            edges.add(t)
        return edges

    def find_nodes(self):
        nodes = {}
        for i, node in enumerate(self.file['node_names']):
            
            # SLEAP storing things as byte strings.
            node = node.decode('utf-8')
            nodes[node] = i
        return nodes

    def visible_frames(self):
        v = []
        for i, frame in enumerate(self.file['track_occupancy']):
            # any() checks if a row contains a single True, or equivalent, value.
            if np.any(frame):
                v.append(i)
        return v
        
    def plot_frame(self, frame):

        # Clear the figure, just incase.
        self.axes.clear()

        # Grabbing the ith visible frame.
        # TODO, might have to rethink this logic.
        #frame = self.v[frame]

        # loop over every animal instance in this frame:
        for instance in self.file['tracks'][:, :, :, frame]:
             
            # grab each set of coordinates for every body part
            x = instance[0, :]
            y = instance[1, :]

            # plot them as points.
            self.axes.plot(x, y, 'o')


            # name the points
            for i, node in enumerate(self.file['node_names']):

                # Sometimes the points don't have valid values.
                # Could be because they are hidden from view. 
                if np.isfinite(x[i]) and np.isfinite(y[i]):
                    self.axes.text(x[i], y[i], node.decode('utf-8'))
            
            # plot the edges.
            for edge in self.file['edge_inds']:

                # Just grabbing the indices of edges.
                node1 = edge[0]
                node2 = edge[1]
    
                # plot() can take 2 iterables that represent different axis'. 
                # In this case, the first argument is an array of x coordinates
                # The second, y coordinates. 
                # Plots a line by matching respective elements from each iterable.
                x = (instance[0, node1], instance[0, node2] )
                y = (instance[1, node1], instance[1, node2] )
                self.axes.plot(x, y)
            
    def animate(self, frames=None):

        # If no frames are provided, animate the entire file.
        if frames == None:
            frames = self.v
        elif frames > len(self.v):
            print(f"Error: trying to animate more frames than SLEAP detected.")
            print(f"number of frames with visible instances: {len(self.v)}")
        return animation.FuncAnimation(self.fig, self.plot_frame, frames)
        
if __name__ == '__main__':
    fishy = SLEAP_Instance_Class('fishyanalysis.h5')
    with fishy as f:
        f.plot_frame(0)
        animate = f.animate()
        animate.save('fish_animation.gif', writer='pillow', fps=30)
        plt.show()
