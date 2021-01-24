# AUTOGENERATED! DO NOT EDIT! File to edit: 02_display.ipynb (unless otherwise specified).

__all__ = ['openImg', 'imageSize', 'displayImage', 'displayTarBarImage', 'displayGridRandom']

# Cell

from google.colab import widgets
from .dirView import *
from itertools import islice
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# open image - add to display.py
def openImg(path_image:str):
    return Image.open(path_image)

def imageSize(path_image:str) -> tuple:
    image = openImg(path_image)
    return image.size

# Display image
def displayImage(path_dir:Path, figsize:tuple=(3, 3)) -> None:
    img = str(path_dir)
    image_show = Image.open(img)
    plt.figure(figsize=figsize)
    plt.imshow(image_show)
    plt.show()

# Display image in TarBar format
def displayTarBarImage(path_dir:Path, first:int, last:int, start_last=False, figsize:tuple=(3, 3)) -> None:
    """
        Display image sequence w/Colab widget TarBar (to use only in Colab).
        Args
            path_dir    : path to image directory
            first       : select first image(inclusive) to be diplayed in the sequence of images
            last        : select last image(exclusive) to be diplayed in the sequence of images
            figsize     : H,W of figure size to be displayed
        Return
            None
    """

    _enum_items = list(islice(itemize(path_dir), first, last))
    tb_plt = widgets.TabBar([str(i) for i in range(first, last)], location='start')

    for base_0 in range(0, last-first):
        with tb_plt.output_to(base_0, select=start_last):
            print(f'File name: {Path(_enum_items[base_0][1].name)}')
            print(f'Image Size: {imageSize(Path(_enum_items[base_0][1]))} (H x W)')
            displayImage(Path(_enum_items[base_0][1]), figsize=figsize)

# Display image in Random format
def displayGridRandom(path_dir:Path, total_img:int, grid_row:int=3, grid_col:int=3, figsize:tuple=(3,3)) -> None:
    """
        Display random selected images w/Colab widget Grid (to use only in Colab).
        Args
            path_dir    : path to image directory
            total_img   : total number of images to be displayed
            row         : select number of grid row
            col         : select number of grid column
            figsize     : H,W of figure size to be displayed
        Return
            None
    """
    if total_img > grid_row * grid_col:
                print(f'To diplay {total_img} images, please increase grid row or col number.')
    else:
        pass

    grid = widgets.Grid(grid_row, grid_col) # row x col
    n = len(itemize(path_dir))
    choice = np.random.choice(n, 6, replace=False).tolist()
    index_list = [itemize(path_dir)[i] for i in choice]

    for id, (row, col) in enumerate(grid):
       try:
            print(f'Fname: {Path(index_list[id][1].name)}')
            displayImage(Path(index_list[id][1]), figsize=figsize)
            print(f'Image Size(HxW):{imageSize(Path(index_list[id][1]))}')
       except:
            pass