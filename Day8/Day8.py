import numpy as np

with open("input.txt", "r") as inp:
    inp = [int(x) for x in list(inp.readlines()[0].strip())]
    width, height = 25, 6
    image = np.array_split(inp, len(inp) // (width*height))
    image_c = [np.bincount(image_p) for image_p in image]
    image_min = np.argmin(np.array([(image_p == 0).sum() for image_p in image]), axis=None)

    print(f"Part 1: {image_c[image_min][1] * image_c[image_min][2]}")

    image = [x.reshape(height, width) for x in image]

    for i, img in enumerate(image[1:]):
        img[image[i] < 2] = 0
    image = np.array(image)
    image[image == 2] = 0
    print("Part 2:")
    print(np.sum(np.array(image), axis=0))
