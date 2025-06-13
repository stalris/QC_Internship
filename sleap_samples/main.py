import h5py
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


def get_extrema(matr: np.array) -> tuple:
    # 500 is a general central point (just off of eyeballing)
    (x_maximum, x_minimum) = 500, 500
    (y_maximum, y_minimum) = 500, 500
    instance_tracker = {}
    for instance in range(len(matr)):
        for node in range(len(matr[instance][0])):
            for i in range(len(matr[0][0][0])):
                if matr[instance][0][node][i] < x_minimum:
                    x_minimum = matr[instance][0][node][i]
                elif matr[instance][0][node][i] > x_maximum:
                    x_maximum = matr[instance][0][node][i]

                if matr[instance][1][node][i] < y_minimum:
                    y_minimum = matr[instance][1][node][i]
                elif matr[instance][1][node][i] > y_maximum:
                    y_maximum = matr[instance][1][node][i]


    # for equal aspects, return greater max + greater min
    return (x_minimum if x_minimum < y_minimum else y_minimum,
            x_maximum if x_maximum > y_maximum else y_maximum)


# First iteration of drawing skeletons to a graph
def fly_skeleton(points: np.array, color: str, ax: plt.Axes):
    # head -> thorax
    plt.plot([points[0][0], points[2][0]], [points[0][1], points[2][1]], marker='o', color=color)

    # thorax -> abd
    plt.plot([points[2][0], points[1][0]], [points[2][1],  points[1][1]], marker='o', color=color)

    # Add some patches to show biggest segments
    head = Circle((points[0][0], points[0][1]), radius=5, fc=color)
    ax.add_patch(head)
    thorax = Circle((points[2][0], points[2][1]), radius=10, fc=color)
    ax.add_patch(thorax)
    abd = Circle((points[1][0], points[1][1]), radius=7, fc=color)
    ax.add_patch(abd)

    # thorax -> wings
    plt.plot([points[2][0], points[3][0]], [points[2][1], points[3][1]], marker='o', color=color)
    plt.plot([points[2][0], points[4][0]], [points[2][1], points[4][1]], marker='o', color=color)

    # Wing patches
    wing1 = Circle((points[3][0], points[3][1]), radius=7, fc=color)
    ax.add_patch(wing1)
    wing2 = Circle((points[4][0], points[4][1]), radius=7, fc=color)
    ax.add_patch(wing2)

    # thorax -> right limbs
    plt.plot([points[2][0], points[5][0]], [points[2][1], points[5][1]], marker='o', color=color)
    plt.plot([points[2][0], points[6][0]], [points[2][1], points[6][1]], marker='o', color=color)
    plt.plot([points[2][0], points[7][0]], [points[2][1], points[7][1]], marker='o', color=color)
    # thorax -> left limbs
    plt.plot([points[2][0], points[8][0]], [points[2][1], points[8][1]], marker='o', color=color)
    plt.plot([points[2][0], points[9][0]], [points[2][1], points[9][1]], marker='o', color=color)
    plt.plot([points[2][0], points[10][0]], [points[2][1], points[10][1]], marker='o', color=color)

# Uses a skeleton via the format
fish_skeleton = {
    0: [5],  # base_back
    1: [4, 10],  #spine_front
    2: [],  # tailfin_end
    3: [],  # dorsal_back
    4: [7, 9],  # spine_mid_front
    5: [2],  # tailfin_start
    6: [1, 8],  # l_eye
    7: [3],  # dorsal_front
    8: [0],  # base_front
    9: [5],  # spine_back
    10: [8],  # mouth
    11: [1, 8],  # r_eye
}
# to dynamically create a graph for any skeleton ( i think )
def draw_skeleton(points: np.array, color: str, ax: plt.Axes, mappings):
    for key, val in mappings.items():
        for outnode in val:
            plt.plot([points[key][0], points[outnode][0]], [points[key][1], points[outnode][1]], marker='o', color=color)

# Dimensions of the tracks matrix are
# First: Frame
# Second: Node
# Third: X / Y
# Fourth: instance (fly) number
# Note that data is mirrored
with h5py.File('./fishyanalysis.h5', 'r') as f:
    # occupancy_matrix = f['track_occupancy'][:]
    tracks = f['tracks'][:]
    plot_border = 0.1

    (min, max) = get_extrema(tracks)
    border = min - min * plot_border, max + max * plot_border
    tracks = tracks.transpose()

    fig, ax = plt.subplots()

    colors = ['blue', 'red']
    for frame in range(len(tracks)):
        if frame != 3313:
            continue
        for instance in range(len(tracks[frame][0][0])):
            if instance >= 2:
                continue
            inst_x = []
            inst_y = []
            for node in range(len(tracks[0])):
                inst_x.append(tracks[frame][node][0][instance])
                inst_y.append(tracks[frame][node][1][instance])
            draw_skeleton(list(zip(inst_x, inst_y)), colors[instance], ax, fish_skeleton)
    print("made it to the end")
    plt.show()
