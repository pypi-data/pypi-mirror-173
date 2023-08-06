#!/usr/bin/env python3

import cv2
import logging
import numpy as np
import os.path
import time
from typing import List
from PIL import Image
import pandas as pd
import pathlib
import torch

from bioblu.ds_manage import ds_annotations
from bioblu.main import YOLO_IMG_FORMATS


def cvt_tif_to_png(fdir_src, fdir_dst=None, overwrite=False):
    if fdir_dst is None:
        fdir_dst = fdir_src

    img_fpaths = ds_annotations.get_all_fpaths_by_extension(fdir_src, (".tif", ".tiff",))
    img_count = len(img_fpaths)

    for i, src in enumerate(img_fpaths):
        if (i + 1) % 10 == 0:
            print(f"Completed {i + 1} of {img_count}")
        fname_dst = f"{os.path.splitext(os.path.basename(src))[0]}.png"
        fpath_dst = os.path.join(fdir_dst, fname_dst)
        logging.info(f"Converting tif(f) to png: {src}")
        if not overwrite and os.path.exists(fpath_dst):
            print(f"Skipped existing file: {fpath_dst}")
            continue
        cv2.imwrite(fpath_dst, cv2.imread(src))


def cvt_all_tif_to_png(fdir):
    fpaths = ds_annotations.get_all_fpaths_by_extension(fdir, YOLO_IMG_FORMATS)
    for src in fpaths:
        dst = os.path.splitext(src)[0] + ".png"
        cv2.imwrite(dst, cv2.imread(src))


def rotate_img_by_deg(img, deg):
    try:
        vres, hres, channels = img.shape
    except AttributeError:
        print("Could not extract image dimensions. Returning input unchanged.")
        return img
    else:
        img_center_xy = (hres * 0.5, vres * 0.5)
        rotation_matrix = cv2.getRotationMatrix2D(center=img_center_xy, angle=deg, scale=1.0)

        # from https://stackoverflow.com/a/47248339
        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_matrix[0, 0])
        abs_sin = abs(rotation_matrix[0, 1])
        # find the new width and height bounds
        bound_w = int(vres * abs_sin + hres * abs_cos)
        bound_h = int(vres * abs_cos + hres * abs_sin)
        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_matrix[0, 2] += bound_w / 2 - img_center_xy[0]
        rotation_matrix[1, 2] += bound_h / 2 - img_center_xy[1]

        img_rot = cv2.warpAffine(img, rotation_matrix, (bound_w, bound_h))
        return img_rot


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    """From: https://stackoverflow.com/a/44659589"""
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def fit_and_pad(img_in: np.ndarray, new_dims_yx: tuple, pad_col=(0.5, 0.5, 0.5)):
    assert len(img_in.shape) == 3
    # Resize to fit into target dims
    target_height, target_width = new_dims_yx
    height_old, width_old, _ = img_in.shape
    horz_rescale_factor = target_width / width_old
    vert_rescale_factor = target_height / height_old
    if vert_rescale_factor < horz_rescale_factor:
        new_height, new_width = (int(height_old * vert_rescale_factor), int(width_old * vert_rescale_factor))
    else:
        new_height, new_width = (int(height_old * horz_rescale_factor), int(width_old * horz_rescale_factor))
    img_resized = cv2.resize(img_in, (new_width, new_height))  # Note: (width, height), not (height, width)
    new_height, new_width, _ = img_resized.shape
    # Pad image
    pad_width_left = pad_width_right = int((target_width - new_width) * 0.5)
    pad_height_top = pad_height_bottom = int((target_height - new_height) * 0.5)
    img_out = cv2.copyMakeBorder(img_resized, pad_height_top, pad_height_bottom, pad_width_left, pad_width_right,
                                 borderType=cv2.BORDER_CONSTANT, value=pad_col)
    return img_out

def get_all_img_dims(fdir_root) -> pd.DataFrame:
    fpaths_imgs = ds_annotations.get_all_fpaths_by_extension(fdir_root, YOLO_IMG_FORMATS)
    widths, heights = [], []
    for fpath in fpaths_imgs:
        width, height = Image.open(fpath).size
        widths.append(width)
        heights.append(height)
    img_data = pd.DataFrame({
        "fpath": fpaths_imgs,
        "width": widths,
        "height": heights,
    })
    img_data["fname"] = img_data["fpath"].apply(lambda f: os.path.split(f)[-1])
    img_data["area"] = img_data["width"] * img_data["height"]
    print(img_data.columns)
    return img_data


# def find_smallest_img(fpath_root) -> List[dict]:
#     """
#     Finds the smalles image(in terms of area).
#     :param fpath_root: root path to look for images
#     :return: [{"height": <int>, "width": <int>, "area": <int>, "fpath": <str>}]
#     """
#     smallest_area = None
#     smallest_imgs = []
#     img_fpaths = ds_annotations.get_all_fpaths_by_extension(fpath_root, YOLO_IMG_FORMATS)
#     if not img_fpaths:
#         print("No img. files found.")
#     img_count = len(img_fpaths)
#     for i, fpath in enumerate(img_fpaths):
#         # height, width, _ = cv2.imread(fpath).shape
#         width, height = Image.open(fpath).size
#         logging.debug(f"Width: {width}, height: {height}, img: {fpath}")
#         img_dict = {
#             "width": width,
#             "height": height,
#             "area": width * height,
#             "fpath": fpath,
#         }
#         if smallest_area is None and not smallest_imgs:  # Initiate
#             smallest_area = width * height
#             smallest_imgs.append(img_dict)
#         elif smallest_area > img_dict["area"]:  # If new image is smaller
#             smallest_area = img_dict["area"]
#             smallest_imgs = [img_dict]
#         elif smallest_area == img_dict["area"]:  # If image is same size as previous smallest:
#             smallest_imgs.append(img_dict)
#         elif smallest_area < img_dict["area"]:
#             pass
#         else:
#             print(f"Error comparing size of img {fpath}")
#         logging.debug(f"Smallest area: {smallest_area}")
#
#         if (i + 1) % 50 == 0:
#             print(f"Checked {i + 1} of {img_count} imgs.")
#     print(f"Done.")
#     return smallest_imgs


def get_largest_imgs(fdir_root):
    img_data = get_all_img_dims(fdir_root)
    max_area_rows = img_data[img_data["area"] == img_data["area"].max()]
    return max_area_rows


def get_smallest_imgs(fdir_root):
    img_data = get_all_img_dims(fdir_root)
    min_area_rows = img_data[img_data["area"] == img_data["area"].min()]
    return min_area_rows


if __name__ == "__main__":
    loglevel = logging.DEBUG
    logformat = "[%(levelname)s]\t%(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    logging.disable()
    pd.options.display.width = 0

    # target_dims = (512, 640)
    #
    # fpath_img = "/home/findux/Pictures/huleeb-560-09-jul-2021-final-c.jpg"
    # cv2.imshow("fig", fit_and_pad(cv2.imread(fpath_img), new_dims_yx=(512, 640)))
    # cv2.waitKey(0)
    # fpath_img = "/media/findux/DATA/Pictures/1696e0b28a1675b1adb1c77137dcfc5a63f932d0-scaled.jpg"
    # cv2.imshow("fig", fit_and_pad(cv2.imread(fpath_img), new_dims_yx=(512, 640)))
    # cv2.waitKey(0)
    # fpath_img = "/media/findux/DATA/Pictures/cXJDTxismall.jpg"
    # cv2.imshow("fig", fit_and_pad(cv2.imread(fpath_img), new_dims_yx=(512, 640)))
    # cv2.waitKey(0)

    fdir_root = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_17_yolo/"
    # fdir_root = "/home/findux/Pictures/Webcam/"
    # imgs = find_smallest_img(fdir_root)
    largest = get_largest_imgs(fdir_root)
    print(largest)
    smallest = get_smallest_imgs(fdir_root)
    print(smallest)