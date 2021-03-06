# AUTOGENERATED! DO NOT EDIT! File to edit: 05_imageTools.ipynb (unless otherwise specified).

__all__ = ['viewMask', 'findCenter', 'findDiskCoord', 'preComposite', 'compositeBuild', 'findContours',
           'contours2Segmentations', 'seg2BBoxArea', 'findCoord', 'compositeImage', 'imgCompSegBbox']

# Cell
import pandas as pd
import numpy as np

from shapely.geometry import Polygon, MultiPolygon
from PIL import Image
from dataclasses import dataclass, field
from .display import *
from .dirView import *
from skimage import measure
from pathlib import Path


# Display output mask
def viewMask(path_image:Path, path_mask:Path, new_mask) -> None:
    fname = path_image.stem + ".png"
    mask_path = path_mask.joinpath(fname)
    new_mask.save(mask_path)

# Find center of image(i.e. zone of inhibition)
def findCenter(path_image:Path, coord:tuple) -> int:
    fore_img_size = imageSize(path_image)
    center_x = coord[0] + fore_img_size[0]//2
    center_y = coord[1] + fore_img_size[1]//2
    return center_x, center_y

# Find coordinate of disk on top of zone of inhibition
def findDiskCoord(path_image:Path, center_x:int, center_y:int) -> int:
    fore_img_size = imageSize(path_image)
    coord_x = center_x - fore_img_size[0]//2
    coord_y = center_y - fore_img_size[1]//2
    return coord_x, coord_y

# Preprocess image for composite
def preComposite(path_image:Path, coord:tuple, img_size:tuple, back:Path, index_name:str):
    fore_img = Image.open(path_image)
    fore_img_size = imageSize(path_image)
    new_fore = Image.new("RGBA", img_size , color=(0, 0, 0, 0))
    new_fore.paste(fore_img, tuple(coord))
    new_mask = Image.new("L", img_size, color=0)
    # Get the alpha channel image.
    fore_img_mask = fore_img.getchannel(3)
    # Paste the foreground alpha into the new mask.
    new_mask.paste(fore_img_mask, tuple(coord))
    #viewMask(image, mask_path, new_mask)
    background = Image.open(back)
    return new_fore, background, new_mask, index_name

# Create composite image
def compositeBuild(new_fore, back, new_mask, fname:str, train_path:Path):
    # Composite image is blended from a foreground, background and mask, all of the same size.
    composite_img = Image.composite(new_fore, back, new_mask)
    # Save the new composited image.
    path_composite = train_path.joinpath(fname)
    composite_img.save(path_composite)
    return new_mask

# Find foreground image contour
def findContours(new_mask, coord):
    contours = measure.find_contours(new_mask, 0.8)
    new_contours = []
    for cont in contours:
        for i in range(len(contours[0])):
            _contours = (cont[i][1], cont[i][0])
            new_contours.append(_contours)

    new_contours_array = np.array(new_contours)
    re = new_contours_array.shape[0]
    new_contours_array = new_contours_array.reshape(-1, re, 2)
    return new_contours_array, new_contours_array.size

# Convert contour to segmentation
def contours2Segmentations(contours_array, tolerance:int=1.0, preserve_topology:bool=False):
    segmentations = []
    polygons = []

    for contour in contours_array:
        poly = Polygon(contour)
        poly = poly.simplify(tolerance, preserve_topology=preserve_topology)
        polygons.append(poly)
        seg = np.array(poly.exterior.coords).ravel().tolist()
        segmentations.append(seg)
    return polygons, segmentations

# Convert segmentation to bounding box area
def seg2BBoxArea(polygons):
    multi_poly = MultiPolygon(polygons)
    x, y, max_x, max_y = multi_poly.bounds
    width = max_x - x
    height = max_y - y
    bbox = [x, y, width, height]
    area = multi_poly.area
    return [bbox, area]

# Cell
def findCoord(images:list, coord:tuple) -> tuple:
    center_x, center_y = findCenter(images[0], coord)
    disk_x, disk_y = findDiskCoord(images[1], center_x, center_y)
    return (disk_x, disk_y)

def compositeImage(path_image:Path, coord:tuple, img_size:tuple, back:Path, fname_train:str, train_path:Path, index_name:str):
    new_fore, background, new_mask, index_name = preComposite(path_image, coord, img_size, back, index_name)
    mask = compositeBuild(new_fore, background, new_mask, fname_train, train_path)
    return mask, index_name

def imgCompSegBbox(path_image:Path, coord:tuple, img_size:tuple, back:Path, fname_train:str, train_path:Path, index_name:str):
    mask, index_name = compositeImage(path_image, coord, img_size, back, fname_train, train_path, index_name)
    contours_array, countours_size = findContours(mask, coord)
    polygons, segmentation = contours2Segmentations(contours_array, tolerance=1.0, preserve_topology=False)
    bbox, area = seg2BBoxArea(polygons)
    return bbox, area, segmentation, index_name