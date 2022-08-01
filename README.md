# 3D-annotation-image-upscaler-for-huge-images
## code snippet to upscale an 3D annotation file to TB size independed of working memory (PROOF-OF-CONCEPT)

Some python code to upscale an annotation image to a high resolution image without loosing the annotation labels. I'm not a programmer and I still hope to find someone solving this task before so I didn't have to write such bad code. But after more than a year of unsuccessful searching, i was forced to solve the problem myself. Note how often this question arises in neuroscience, which is why it is unlikely that it has not been solved by anyone.

The code is mostly based on the memmap function of numpy and it upscales in 2 Dimensions per Step using the [resize function of Pillow package](https://pillow.readthedocs.io/en/stable/reference/Image.html) and rotate the Image virtually after the Steps to upscale the whole 3D Image. This makes it possible to upscale an image to nearly unlimited size. I successfully upscaled an image from 300 MB into an 450 GB image using a PC with 8 GB RAM in under an hour (about 120MB write/s).

## Why to care?:

I registered a huge lightsheet brain dataset from a mouse onto the allen mouse brain atlas ([Wang et al. 2020 Cell](https://doi.org/10.1016/j.cell.2020.04.007)) or vice versa. To perform this task you currently have to downscale the image, besides, it does not increase the registration quality since the atlas is currently only offered in 10um resolution. I segmented the vessels or counted the cells (i.e. using [Kirst et al. 2020 Cell](https://doi.org/10.1016/j.cell.2020.01.028)) after that i wanted to show the cells in dependence of the brain region, because this was the aim of the registration. Important to know: you have to disable any kind of interpolation algorithm, it makes the annotations unusable. 

The result should look similar to this ([Blue Brain Cell Atlas](https://bbp.epfl.ch/nexus/cell-atlas/)):
<p align="center">
<a href="https://bbp.epfl.ch/nexus/cell-atlas/">
<img src="https://christophkirst.github.io/3D-annotation-image-upscaler/3D-AIUdocs/blue_brain_cell_atlas_example1.png" 
 alt="Blue Brain Cell Atlas Example" width="300" hspace="40"/></a>

To my great surprise there was no function to do this in neither Imaris nor Arivis (very high-quality proprietary software systems for the display and processing of particularly large neuroscientific image data). In ImageJ you could do this using the *scale function* but it uses the working memory, so large images are impossible and also the performance seems pretty bad. [Convert3D from the authors of itk-snap](http://www.itksnap.org/pmwiki/pmwiki.php?n=Downloads.C3D) can upscale images slices wise and disable the interpolation, but it can only upscale images with less then 256 colors and is incapable to upscale images larger then some GB.

## Next steps?:

- parallelizing the algorithm (depending on the speed of the disc drive)
- use N5 or HDF5 to save the data for better performance and data storage
- combine the upscaler and the cell plotter (work in progress)
- integrate the upscaler into Arivis to plot the cells depending on a specific region
