import h5py as h5
import numpy as np
import matplotlib.pyplot as plt

try:
    with h5.File('test.h5', 'w') as file:
        dataset = np.array([
            [
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]
            ],
            [
                [10, 20, 30, 40],
                [50, 60, 70, 80],
                [90, 100, 110, 120]
            ]

        ])
        
        file.create_dataset('test_dataset', data=dataset)
except FileExistsError:
    # do nothing.
    pass

with h5.File('test.h5', 'r') as file:
    print(f"file['test_dataset']: \n\t{file['test_dataset']}")
    print()


    # prints all of the contents.
    print(f"file['test_dataset'].shape: \n\t{file['test_dataset'].shape}")
    print(f"contents of file['test_dataset'][:]: \n{file['test_dataset'][:]}")
    print()

    # print out the contents of the first element in the first index.
    print(f"print the contents of the first element in the first index.")
    print(f"file['test_dataset'][0, :, :].shape: \n\t{file['test_dataset'][0, :, :].shape}")
    print(f"file['test_dataset'][0, :, :]: \n{file['test_dataset'][0, :, :]}")
    print()

    # print the contents of only the 2nd elements in the 2nd index.
    print(f"print the contents of only the 2nd element in the 2nd index")
    print(f"file['test_dataset'][:, 1, :].shape: \n\t{file['test_dataset'][:, 1, :].shape}")
    print(f"file['test_dataset'][:, 1, :]: \n{file['test_dataset'][:, 1, :]}")
    print()

    # print the last element of the last index.
    print(f"print the last element of the last index.")
    print(f"file['test_dataset'][:, :, 3].shape: \n\t{file['test_dataset'][:, :, 3].shape}")
    print(f"file['test_dataset'][:, :, 3]: \n{file['test_dataset'][:, :, 3]}")
    print()


# find the first visible frame in the fly dataset.

with h5.File('fly.h5', 'r') as fly:

    print(f"print the datasets in the fly.h5 file: ")
    for dataset in fly:
        print(dataset)
    print()

    print(f"find all the frames where SLEAP detected at least one animal instance")
    print(f"fly['track_occupancy'].shape: \n\t{fly['track_occupancy'].shape}")
    visible_frames = []
    # enumerate allows you to pair each for loop with a counter.
    for i, occupancy_array in enumerate(fly['track_occupancy']):
        if np.any(occupancy_array):
            visible_frames.append(i)

    print(f"what is the first frame where sleap detected an animal?")
    print(f"visible_frames[0]: \n\t{visible_frames[0]}")
    
    print(f"plotting the first frame.")

    # create a figure an axes in order to plot things.
    fig, axes = plt.subplots()

    # loop over each animal for the first frame.
    for animal in fly['tracks'][:, :, :, visible_frames[0]]:
    
        print(f"animal.shape: \n\t{animal.shape}")
        #  grab the x coordinates for each body part.
        x = animal[0, :]

        # grab the y coordiantes for each body part.
        y = animal[1, :]

        # plot them as points using matplotlib. Requires the 'o' argument.
        axes.plot(x, y, 'o')

    # once drawing on the canvas is down, show it
    plt.show()
