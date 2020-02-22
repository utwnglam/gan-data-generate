# Use of stylistic GAN in Gaming Applications
Data processing reference of FYP

## Generator
Generate png which represent 3D voxel cube

1st version: Generate png contain 2D square only

**IKEA dataset:**

dataset from [Dataset for IKEA 3D models and aligned images](http://people.csail.mit.edu/lim/paper/lpt_iccv2013.pdf)

change `.obj` files to `.binvox` by [binvox](http://www.google.com/search?q=binvox)

read and retrieve the numpy array of `.binvox` by [binvox-rw-py](https://github.com/pclausen/binvox-rw-py)

>Put desired `.binvox` files inside folder `/BINVOX/INPUT/`
>then result `.png` will be in folder `/BINVOX/OUTPUT/`

remember to change the function first
```
if __name__ == "__main__":
    ikea_convert()
```

## Visualizer
Convert 2D result png back to 3D voxel for visualization
