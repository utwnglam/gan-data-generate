import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import sys
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

RESO = 30
RATIO = 3
TOTAL = RESO * RATIO
iteration = 0

#
# OPEN THE TARGET PNG
#
img = Image.open('result/output_0.png')
data = np.array(img)

#
# CONVERT THE 2D PNG TO ARRAY THAT CAN BE REPRESENT BY VOXEL
#
data = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))
data = data[::3, ::3, ::3, 0:]
colors = np.divide(data, 255)

cube = np.zeros((RESO, RESO, RESO), dtype=bool)
transparent = np.array([1, 1, 1])

for i in range(colors.shape[0]):
    for j in range(colors.shape[1]):
        for k in range(colors.shape[2]):
            if not np.array_equal(colors[i][j][k], transparent):
                cube[i][j][k] = True

#
# PLOTTING THE GRAPH TO MAKE SURE VOXEL IS NORMAL
#
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(cube, facecolors=colors, edgecolor='grey')
plt.savefig('voxel_' + str(iteration) + '.png')
plt.show()
