#!/usr/bin/env

import os
import pathlib
from bioblu.main import IMG_FORMATS
from bioblu.ds_manage import ds_annotations

def initiate_archive(fpath_TACO, archive_fname="img_archive.txt"):
    fpath_TACO = os.path.normpath(fpath_TACO)
    fpath_archive = "/" + os.path.join(*fpath_TACO.split(os.sep)[:-1]) + f"/{archive_fname}"
    fdir_data = os.path.join(fpath_TACO, "data")
    img_paths = ds_annotations.get_all_fpaths_by_extension(fdir_data, IMG_FORMATS)
    img_paths = [e + "\n" for e in img_paths]
    if os.path.exists(fpath_archive):
        input(f"Warning! Archive already exists: {fpath_archive}\nPress [ENTER] to overwrite.")
    with open(fpath_archive, "w") as f:
        f.writelines(img_paths)


if __name__ == "__main__":
    fdir_taco = "/media/findux/DATA/Documents/Malta_II/datasets/TACO/TACO/"
    initiate_archive(fdir_taco)

