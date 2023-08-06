#!/usr/bin/env python3

import torch
import json
import pickle



def visualize_model_architecture(pkl_fpath):
    with open(pkl_fpath, "rb") as f:
        model_obj = f.read()
    weights = pickle.loads(model_obj, encoding='latin1')
    [print(e) for e in weights["model"].keys()]

    # model = torch.load(weights)



if __name__ == "__main__":
    fpath = "/media/findux/DATA/Documents/Malta_II/resnet101/model_final_f97cb7.pkl"
    visualize_model_architecture(fpath)