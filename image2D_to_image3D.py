
import numpy as np
from pyface.api import GUI
from mayavi import mlab

def convent_from_2D_to_3D(image2D, color_mode=False, mode="slice", cufoff = 128):
    model = np.zeros((64, 64, 64, 3))
    for i in range(8):
        for j in range(8):
            for a in range(64):
                for b in range(64):
                    if np.all(image2D[i * 64 + a][j * 64 + b] < cufoff):
                        model[a][b][ (7 - i) * 8 + ( 7 - j)] = image2D[i * 64 + a][j * 64 + b]
                    else:
                        model[a][b][ (7 - i) * 8 + ( 7 - j)] = [255,255,255]
    boolean_table = convent_from_3Darray_color_to_boolean(model)
    if(color_mode):
        xx, yy, zz = np.where(boolean_table == 1)
        s = np.arange(len(xx))
        lut = np.zeros((len(xx), 4))
        for row in s:
            temp = np.append((model[xx[row]][yy[row]][zz[row]] + (256-208)), 255)
            lut[row, :] = temp
        # Plot the points, update its lookup table
        currfig = mlab.points3d(xx, yy, zz, s,
                                scale_mode='none',
                                mode="cube",
                                scale_factor=1)
        fig = mlab.figure(1, size=(512, 555))
        currfig.module_manager.scalar_lut_manager.lut.number_of_colors = len(s)
        currfig.module_manager.scalar_lut_manager.lut.table = lut
        mlab.view(azimuth=315, elevation=65, distance=140, focalpoint=(32, 32, 32))
        fig.scene.camera.parallel_projection = True
        fig.scene.camera.parallel_scale = 65    # smaller the number, greater zoom
        mlab.axes(figure=fig, nb_labels=5, extent=(0, 64, 0, 64, 0, 64))
        mlab.outline(extent=(0, 64, 0, 64, 0, 64))
        GUI().process_events()
        imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
        img_RGB = np.uint8(imgmap_RGB)
        mlab.clf()
        return img_RGB
    else:
        xx, yy, zz = np.where(boolean_table == 1)

        fig = mlab.figure(1, size=(512, 555))
        mlab.points3d(xx, yy, zz,
                      color=(0, 1, 0),
                      mode="cube",
                      scale_factor=1)
        mlab.view(azimuth=225, elevation=70, distance=140, focalpoint=(32, 32, 32))
        fig.scene.camera.parallel_projection = True
        fig.scene.camera.parallel_scale = 65
        mlab.axes(figure=fig, nb_labels=5, extent=(0, 64, 0, 64, 0, 64))
        mlab.outline(extent=(0, 64, 0, 64, 0, 64))
        GUI().process_events()
        imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
        img_RGB = np.uint8(imgmap_RGB)
        mlab.clf()
        return img_RGB
        
def convent_from_3Darray_color_to_boolean(color_array):
    if(len(color_array.shape) == 4):
        color_array_x, color_array_y, color_array_z,junk = color_array.shape
    elif(len(color_array.shape) == 3):
        color_array_x, color_array_y, color_array_z = color_array.shape
    boolean_array = np.zeros((color_array_x, color_array_y, color_array_z), dtype=bool)
    for x in range(color_array_x):
        for y in range(color_array_y):
            for z in range(color_array_z):
                boolean_array[x][y][z] = judgement_cutoff_boolean(color_array[x][y][z])
    return boolean_array

def judgement_cutoff_boolean(pixel, cutoff = 128):
    if(pixel[0] >= 128 and pixel[1] >= 128 and pixel[0] >= 128):
        return False
    else:
        return True

