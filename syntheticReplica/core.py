# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['PreviewFore', 'SyntheticImageBuild']

# Cell
from .dirView import *
from .display import *
from .utils import *
from .generate_coordinate import *
from .imageTools import *
from .toolsCOCO import *

import collections
import matplotlib.pyplot as plt
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
import pandas as pd
import random

from dataclasses import dataclass, field
from pathlib import Path
# from PIL import Image
# from shapely.geometry import Polygon, MultiPolygon
# from skimage import measure

@dataclass
class PreviewFore(UtilsBuildLinearCoord):
    path_dir: Path
    file_csv: str
    file_image: str
    dataframe_path: Path = field(init=False, repr=False)
    path_image: Path = field(init=False, repr=False)


    def __post_init__(self):
        self.dataframe_path: Path = Path(self.path_dir).joinpath(self.file_csv)
        self.path_image: Path = Path(self.path_dir).joinpath(self.file_image)
        df = pd.DataFrame(columns = ['init_pto_x', 'init_pto_y', 'expand_x', 'expand_y'], dtype=np.int16)
        df.to_csv(self.dataframe_path, index=True)
        #return self.dataframe_path, self.path_image

    def petriAnnot(self, init_pto, expand_x=1, expand_y=1):
        fig = plt.figure()
        image_show = UtilsBuildLinearCoord.openImg(self.path_image)
        ax = plt.gca()
        # Todo, set max counter to 8
        counter = 0
        for init, x, y in zip(init_pto, expand_x, expand_y):
            _x, _y = UtilsBuildLinearCoord.buildAnnotPoint(init, x, y)
            generate = UtilsBuildLinearCoord.convertMatplot(init, _x, _y)
            store_ptos = UtilsBuildLinearCoord.storeXY(generate)
            color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w' ]
            ax.plot(store_ptos[0], store_ptos[2], '-', color=color[counter])
            ax.plot(store_ptos[1], store_ptos[3], '-', color=color[counter])
            ax.plot(init[0], init[1], marker='o', color=color[counter])
            #ax.text(init[0]-18, init[1]-18, str(counter))
            # Todo: convert text(above line) to color or coordinate
            x_show = (init[0])
            y_show = (init[1])
            ax.text(init[0]-18, init[1]-18, (x_show, y_show))
            #ax.text(init[0]-18, init[1]-18, color[counter])

            counter += 1
        plt.imshow(image_show)
        plt.show()

    # Todo, show image size
    def adPto(self, index:str, init_pto:list, expand_x=1, expand_y=1) -> None:
        df_addPto = pd.read_csv(self.dataframe_path, index_col=0)
        x_pto = init_pto[0]
        y_pto = init_pto[1]
        df_addPto.loc[index] = {'init_pto_x':x_pto, 'init_pto_y':y_pto, 'expand_x':expand_x, 'expand_y':expand_y}
        df_addPto.to_csv(self.dataframe_path, index=True)
        print(df_addPto.head(8))
        init_pto, expand_x, expand_y = UtilsBuildLinearCoord.col2List(self.dataframe_path)
        self.petriAnnot(init_pto, expand_x, expand_y)

    def rmPto(self, index:str ) -> None:
        df_remPto = pd.read_csv(self.dataframe_path, index_col=0)
        df_remPto.drop([index], inplace=True)
        df_remPto.to_csv(self.dataframe_path, index=True)
        print(df_remPto.head(8))
        update_init_pto, update_expand_x, update_expand_y = UtilsBuildLinearCoord.col2List(self.dataframe_path)
        self.petriAnnot(update_init_pto, update_expand_x, update_expand_y)

# Todo: add parameters for multiple supercategory, category_id, category_name
@dataclass
class SyntheticImageBuild:
    image_id: int # synthetic image id
    fname_train: str # file name of synthetic image
    path_train: Path # path to directory in which to strore synthetic images
    original_background: Path # path to directory where petri(background) images are stored
    path_annotation_file: Path # path to file where annotation file is stored
    fore_zone: Path # path where zone(foreground) images are stored
    fore_disk: Path # path where disk(foreground) images are stored
    synthetic_train_path: Path = field(init=False, repr=False) # path_train + fname_train
    is_crowd: int = field(default=0)
    category_zone: int = field(default=0)
    category_disk: int = field(default=1)

    def __post_init__(self):
        self.synthetic_train_path = Path(self.path_train).joinpath(self.fname_train)
        self.back_img_size = imageSize(str(self.original_background))
        self.index_name_list, self.coordinates_list = randomCoordinates(self.path_annotation_file)


    def buildImage(self):
        foreground_sequence = [self.fore_zone, self.fore_disk, self.fore_disk]
        counter = 0
        result = []

        for i in range(len(self.coordinates_list)):
            coord = self.coordinates_list[i]
            random_pick = list(map(lambda x: random.choices(x), foreground_sequence))
            first_selection = [random_pick[0] + random_pick[1]]
            second_selection = [random_pick[2]]
            selection = [first_selection, second_selection]
            _pick = random.choice(random.choices(selection, weights=map(len, selection))[0]) # dtype:list
            pick_size = list(_pick)

            if len(pick_size) == 1:
                #print(f'length 1 {_pick[0]}')
                if counter == 0:
                    # back = background_original
                    bbox, area, segmentation, index_name  = imgCompSegBbox(_pick[0], coord, self.back_img_size, self.original_background, self.fname_train, self.path_train, self.index_name_list[i])
                    counter += 1
                    result.append([segmentation, self.is_crowd, area, self.image_id, bbox, self.category_disk, counter])
                elif counter >= 1:
                    # back = background_train
                    bbox, area, segmentation, index_name = imgCompSegBbox(_pick[0], coord, self.back_img_size, self.synthetic_train_path, self.fname_train, self.path_train, self.index_name_list[i])
                    counter += 1
                    result.append([segmentation, self.is_crowd, area, self.image_id, bbox, self.category_disk, counter])

            elif len(pick_size) == 2:
                #print(f'length 2 {_pick}')
                # starts with background_original
                if counter == 0:
                    # background_original, _pick[0]
                    bbox_zone, area_zone, segmentation_zone, index_name_zone = imgCompSegBbox(_pick[0], coord, self.back_img_size, self.original_background, self.fname_train, self.path_train, self.index_name_list[i])
                    counter += 1
                    result.append([segmentation_zone, self.is_crowd, area_zone, self.image_id, bbox_zone, self.category_zone, counter])

                    coord_disk = findCoord(_pick, coord)
                    bbox_disk, area_disk, segmentation_disk, index_name_disk = imgCompSegBbox(_pick[1], coord_disk, self.back_img_size, self.synthetic_train_path, self.fname_train, self.path_train, self.index_name_list[i])
                    counter += 1
                    result.append([segmentation_disk, self.is_crowd, area_disk, self.image_id, bbox_disk, self.category_disk, counter])

                # starts with background_train
                elif counter >= 1:
                    # background_train, pick[0]
                    bbox_zone, area_zone, segmentation_zone, index_name_zone = imgCompSegBbox(_pick[0], coord, self.back_img_size, self.synthetic_train_path, self.fname_train, self.path_train, self.index_name_list[i])
                    counter += 1
                    result.append([segmentation_zone, self.is_crowd, area_zone, self.image_id, bbox_zone, self.category_zone, counter])

                    # background_train, pick[1]
                    coord_disk = findCoord(_pick, coord)
                    bbox_disk, area_disk, segmentation_disk, index_name_disk = imgCompSegBbox(_pick[1], coord_disk, self.back_img_size, self.synthetic_train_path, self.fname_train, self.path_train, self.index_name_list[i])
                    counter += 1
                    result.append([segmentation_disk, self.is_crowd, area_disk, self.image_id, bbox_disk, self.category_disk, counter])
        return result

    def _annotJSON(self,_result):
        dict_res = []
        for i in range(len(_result)):
            dict_list = addAnnotDict(segmentation=_result[i][0],
                        iscrowd=_result[i][1],
                        area=_result[i][2],
                        image_id=_result[i][3],
                        bbox=_result[i][4],
                        category_id=_result[i][5],
                        id=_result[i][6])

            annot_res = dict_list['annotations'][0]
            dict_res.append(annot_res)
        return dict_res

    def _imageJSON(self):
        images_dic = addImagesDict(self.path_train, self.fname_train, self.image_id)
        return images_dic['images'][0]

    # Todo: add parameters for multiple supercategory, category_id, category_name
    # Make sure you can execute this only once.  Use yield!
    def _catJSON(self):
        # First category
        supercategory = "none"
        id_zone = 0
        name_zone = "zone"
        category_zone_dict = addCatDict(supercategory, id_zone, name_zone)
        zone_dict = (category_zone_dict['categories'][0])
        # Second category
        supercategory = "none"
        id_disk = 1
        name_disk = "disk"
        category_disk_dict = addCatDict(supercategory, id_disk, name_disk)
        disk_dict = (category_disk_dict['categories'][0])
        # Make sure you execute this only once, otherwise it will append new categories.
        categories_dict = {'categories':[]}
        categories_dict['categories'].append(zone_dict)
        categories_dict['categories'].append(disk_dict)
        cat_0 = categories_dict['categories'][0]
        cat_1 = categories_dict['categories'][1]
        return [cat_0, cat_1]

    def JSON2COCO(self, json_fname):
        coco_json = {"images":[], "categories":[], "annotations":[]}
        coco_json['images'].append(self._imageJSON())
        coco_json['categories'].append(self._catJSON()[0])
        coco_json['categories'].append(self._catJSON()[1])

        #annotations_coco = [annot_dict_AML_25, annot_dict_CT5_zone, annot_dict_CT25_diskZone]
        annotations_coco = self._annotJSON(self.buildImage())
        for _annot in annotations_coco:
            coco_json['annotations'].append(_annot)

        # Save to image annotation in coco_annotation directory.
        json_coco = json.loads(json.dumps(coco_json, indent=4))
        synthetic_json = coco_annot_path.joinpath(json_fname)
        with open(synthetic_json, 'w') as coco:
            json.dump(json_coco, coco, indent=4)

        return coco_json
