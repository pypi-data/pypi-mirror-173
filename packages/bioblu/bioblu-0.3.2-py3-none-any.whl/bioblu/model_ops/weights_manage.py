#!/usr/bin/env python3
import torch
import sys

def get_class_names_from_yolo_weights(fpath_yolo_model_weights: str, yolo_dir: str) -> list:
    sys.path.insert(0, yolo_dir)
    weights = torch.load(fpath_yolo_model_weights)
    names: list = weights["model"].names
    return names




if __name__=="__main__":
    fpath_model = "/media/findux/DATA/Documents/Malta_II/results/3816_2022-02-26_000000/exp/weights/best.pt"
    sys.path.insert(0, "/media/findux/DATA/Documents/Malta_II/yolov5/")
    model = torch.load(fpath_model)
    print(model["model"].names)
    model["model"].names = ["trash"]
    torch.save(model, f"{fpath_model.rsplit('.')[0]}_categories_renamed.pt")