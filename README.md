# Antibiogram Composite Images  
> Building composite images


A project with a start up in the micro-biology industry led me to write
some simple form of tooling to automate the production of composite images.  Image compositing is often used to combine related visual elements such as form, shape, color, pattern, or texture, from different sources of images into a single image.  In its elementary form, composite image is the result of blending two images, one on top of the other.<br>

The one on the top is called foreground and the bottom one, the background(Figure 1).  Foreground image is smaller in sizes.  It can also be described as active, when compared to background.  The same foreground image can be used many times and allocated in different locations of the background image during production of composite images.  Background image, on the other hand, is static.  Similar to foreground, the same background image can be used many times during production of composite images, but it rarely needs any adjustment or change.<br>

Composite images are very useful, especially when real images are in shortage.  It was ideal, in my case, for prototyping!   And also, it is cheaper and sometimes easier to obtain than real images.  Nonetheless, hardly composite images can fully substitute real images.  Probably, a combination of both would be ideal for certain scenario.<br> 


* [Training Detectron2 using composite antibiogram images]() (Under construction!)<br>
* Compositing images methods and utility functions:<br> 
  **Sample_nb_1.ipynb**<br>
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/chho-work/syntheticReplica/blob/main/sample_nbs/Sample_nb_1.ipynb) 

  **Sample_nb_2.ipynb**<br>
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/chho-work/syntheticReplica/blob/main/sample_nbs/Sample_nb_2.ipynb)
* [What is "antibiogram"?]() (Under construction!)<br>

## Real vs Composite Images
> Sample of composite images of antibiograms




<img src="https://github.com/chho-work/syntheticReplica/blob/main/assets/real_composite.jpg?raw=True"/>



## Building Composite Images in Practice
> Bottlenecks when making composite images

When creating composite images, I found that it was often the case that I wanted to have the flexibility to choose the number of foreground images. To paste a single  image, I first needed to find a coordinate, the location in the background image.  And obviously,  for each additional image that I choose to paste, more coordinates were required. Time spent generating coordinates soon increased exponentially and it became cumbersome as I built more composite images.   Ideally, this process should be automated.<br>

Initially, I wrote a script to generate random coordinates.  Each random output(coordinates) was randomly selected from coordinates of the background image. In another words, the total possible number of coordinates is equal to image width multiplied by image height.<br>

However, after generating some random coordinates, I realized that this wasn’t going be feasible as some generated coordinates were too close to each other leading foreground images to overlap.  In addition, some few generated coordinates were located out of the petri dish.  Creating a synthetic image with disks and zone of inhibition outside of a petri dish would be out of context and inconsistent with real images(Figure 2).<br>




<img src="https://github.com/chho-work/syntheticReplica/blob/main/assets/composite_image_explain.jpg?raw=True"/>



## Positioning Foreground Images
> The solution, decide in advance the location to paste foreground images

After few more tests, it became clear to me that to solve the above constraints, for each composite image I needed to generate random coordinates that falls within a smaller boundary(range), rather than the image size range.  The boundary would first, limit the locations in which each image would appear and avoid image overlap when it happens. Second, it restricts the areas in which each disk and zone of inhibition would appear, it would locate them inside of the petri dish, making the synthetic image more realistic.<br>

The illustration below depicts the idea.  In this example, there are two boundaries(B1, B2), each for a different foreground image.  Each boundary is limited by the size of horizontal(expand_x) and a vertical(expand_y) lines.  The size of each line is the range of possible coordinates.  The coordinate to paste the foreground image in boundary B1 will be selected randomly from the sequence of coordinates under list B1. And same applies to B2 boundary.<br> 




<img src="https://github.com/chho-work/syntheticReplica/blob/main/assets/positioning.jpg?raw=True"/>



## Try It in Google Colab!
**Sample_nb_2.ipynb**<br>
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/chho-work/syntheticReplica/blob/main/sample_nbs/Sample_nb_2.ipynb)

Position each foreground image:
* To create a new position, create a new name for "index" and add input new coordinates for init_pro, expand_x(optional) and expand_y(optional).
* You can view the position of each coordinate created by executing the cell.
* To update a previously created point, change the index to the name of the point you wish to update and make the approapriate changes.    





<img src="https://github.com/chho-work/syntheticReplica/blob/main/assets/positioning_nb.jpg?raw=True"/>



Make Composite Images:
* "image_id" numbering must start with number 1, 2, 3, ...
* To change the name of the file, simply change the name of "fname_train".
* You can view the names and images for previous created composite images by pressing the numbers in the TarBar.




<img src="https://github.com/chho-work/syntheticReplica/blob/main/assets/build.jpg?raw=True"/>


