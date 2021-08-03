import os

import cv2
import numpy as np

def main():
    data = np.load("data/training_data.npy", allow_pickle=True)
    targets = np.load("data/target_data.npy", allow_pickle=True)

    print(f'Image Data Shape: {data.shape}')
    print(f'targets Shape: {targets.shape}')

    # Lets see how many of each type of move we have.
    unique_elements, counts = np.unique(targets, return_counts=True)
    print(np.asarray((unique_elements, counts)))

    # Store both data and targets in a list.
    # We may want to shuffle down the road.

    holder_list = []
    for i, image in enumerate(data):
        holder_list.append([data[i], targets[i]])


    labelsDirList = {
        "Q": ["Right", "r"],
        "D": ["Left", "l"],
        ",": ["Up", "u"]
    }

    countList = {}

    count_up = 0
    count_left = 0
    count_right = 0
    count_down = 0
    count_start = 0

    for data in holder_list:
        k = data[1]
        if k in labelsDirList.keys():
            kList = labelsDirList[k]
            path = "I:/ia/{}/".format(kList[0])
            if k not in countList.keys():
                countList[k] = 0
            else:
                countList[k] += 1

            if not os.path.isdir(path):
                os.mkdir(path)
            path += "H7-{}{}.png".format(kList[1], countList[k])
            cv2.imwrite(path, data[0])


if __name__ == '__main__':
    main()