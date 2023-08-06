#!/usr/bin/env python3
import datetime
import logging
import os
import pandas as pd

from bioblu import video_processing
from bioblu.main import DRONE_MODELS
from bioblu.ds_manage import ds_annotations
from bioblu.ds_manage import geoprocessing


def predict_video(fpath_video: str, weights_file: str, yolo_repo: str, target_fdir: str = None,
                  use_orig_resolution: bool = False, conf_thresh: float = None, iou_thresh: float = None):

    predict_script = os.path.join(yolo_repo, "detect.py")

    inference_command = f"python3 {predict_script} --source {fpath_video} --weights {weights_file} --save-conf " \
                        f"--save-txt"

    if target_fdir is not None:
        inference_command += f" --project {target_fdir}"
    if use_orig_resolution:
        vid_width, vid_height = video_processing.get_video_resolution(fpath_video)
        inference_command += f" --img-size {int(vid_width)}"
    if conf_thresh is not None:
        inference_command += f" --conf-thres {conf_thresh}"
    if iou_thresh is not None:
        inference_command += f" --iou-thres {iou_thresh}"

    os.system(inference_command)
    # ToDo: Pack all the other things, geolocation etc. in here.


def get_video_predictions_df(fdir_predictions):
    predictions = ds_annotations.load_all_yolo_annotations_only(fdir_predictions)
    predictions = pd.DataFrame(predictions)
    frames = predictions.file_name.str.extract(r".*_(\d+)\.txt", expand=True)
    predictions["frame"] = frames.astype(int)
    return predictions


def join_predictions_and_telemetry(fdir_preds, fpath_srt, remove_nan_rows=False) -> pd.DataFrame:
    predictions = get_video_predictions_df(fdir_preds)
    if os.path.exists(fpath_srt):
        telemetry = video_processing.get_telemetry_df(fpath_srt)
        telemetry = video_processing.get_interpolated_telemetry(fpath_srt)  # ToDo: make this a parameter
        logging.info(f"Telemetry data: {telemetry.shape}. Columns: {telemetry.columns}")
        joined_table = predictions.merge(telemetry, on="frame", how="left")
    else:
        print("[ WARNING ] No srt file found to extract telemetry data from")
        joined_table = predictions
    logging.info(f"Predictions: {predictions.shape}")

    if remove_nan_rows:  # ToDo: MAaybe use a telemetry dict per frame after all, and use .get() to get telemetry for the corresponding frame
        old_row_count = joined_table.shape[0]
        joined_table.dropna(inplace=True)
        new_row_count = joined_table.shape[0]
        print(f"Dropped {old_row_count - new_row_count} rows due to NA values.")
    return joined_table


def geolocate_prediction_boxes(fdir_preds, fpath_srt, fpath_video, sensor_width_mm: float, focal_length_real_mm: float):
    hres, vres = video_processing.get_video_resolution(fpath_video)
    joined_table = join_predictions_and_telemetry(fdir_preds=fdir_preds, fpath_srt=fpath_srt, remove_nan_rows=True)
    logging.info(f"Joined table columns: {joined_table.columns}")
    row_count = joined_table.shape[0]

    joined_table["img_width"] = hres
    joined_table["img_height"] = vres
    joined_table["img_dims_wh"] = [(hres, vres) for i in range(joined_table.shape[0])]
    logging.info(f"Joined table: Columns: {joined_table.columns}")
    if "img_lat" in joined_table.columns:
        joined_table["img_latlon"] = list(zip(joined_table["img_lat"], joined_table["img_lon"]))
        joined_table["bbox_center_x"] = joined_table["bbox"].str[0]
        joined_table["bbox_center_y"] = joined_table["bbox"].str[1]
        joined_table["bbox_center_xy"] = list(zip(joined_table["bbox"].str[0] * joined_table["img_width"],
                                                  joined_table["bbox"].str[1] * joined_table["img_height"]))
        joined_table["GSD_cm"] = geoprocessing.get_gsd(joined_table["internal_altitude"],
                                                       focal_length_real_mm, sensor_width_mm, joined_table["img_width"])
        prediction_latlon = []
        for i, line in joined_table.iterrows():  # For some reason, this does not work columnwise
            if i % 2500 == 0:
                print(f"Processed {i * 100 / row_count:.2f} %")
            current_latlon = geoprocessing.geolocate_point(line["bbox_center_xy"], line["img_dims_wh"],
                                                           line["img_latlon"], line["GSD_cm"], line["yaw"])
            prediction_latlon.append(current_latlon)
        joined_table["pred_latlon"] = prediction_latlon
    # joined_table["latlon"] = geoprocessing.geolocate_point_pandas_friendly(joined_table["bbox_center_x"],
    #                                                                        joined_table["bbox_center_y"],
    #                                                                        joined_table["img_width"],
    #                                                                        joined_table["img_height"],
    #                                                                        joined_table["img_lat"],
    #                                                                        joined_table["img_lon"],
    #                                                                        joined_table["GSD_cm"],
    #                                                                        joined_table["yaw"])
        joined_table["latitude"] = joined_table["pred_latlon"].str[0]
        joined_table["longitude"] = joined_table["pred_latlon"].str[1]
    else:
        logging.info("No lat/lon column found to use for geolocation.")
    return joined_table


def main(fpath_video, fpath_weights, fdir_yolo_repo, output_dir=None, fpath_srt=None, use_orig_resolution=True, conf_thresh=None,
         iou_thresh=None, sensor_width=7.68, focal_length=4.0):

    if output_dir is None:
        tstamp = format(datetime.datetime.now(), "%Y-%m-%d_%H%M")
        video_basename = os.path.split(fpath_video)[-1].rsplit(".")[0]
        weights_basename = os.path.split(fpath_weights)[-1].rsplit(".")[0]
        output_dir = os.path.join(os.path.split(fpath_video)[0], f"predictions_{tstamp}_{weights_basename}_{video_basename}")
    print(f"Saving results to: {output_dir}")

    if fpath_srt is None:
        fpath_srt = os.path.splitext(fpath_video)[0] + ".SRT"
        logging.info(f"Looking for srt file at: {fpath_srt}")

    predict_video(fpath_video, fpath_weights, fdir_yolo_repo, output_dir, use_orig_resolution, conf_thresh, iou_thresh)
    predictions_fdir = os.path.join(output_dir, "exp", "labels")
    logging.info(f"Predictions dir: {predictions_fdir}")

    geolocated_table = geolocate_prediction_boxes(predictions_fdir, fpath_srt, fpath_video, sensor_width_mm=sensor_width,
                                                  focal_length_real_mm=focal_length)
    geolocated_table.to_csv(os.path.join(output_dir, "geolocated_predictions.csv"))
    video_processing.get_telemetry_df(fpath_srt).to_csv(os.path.join(output_dir, "flight_path.csv"))
    return geolocated_table


if __name__ == "__main__":

    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    logging.disable()

    # ToDo: - Add custom resolution
    #       - Make interpolation a parameter (needs to propagate to video_processing)
    #       - Incorporate clustering


    video = "/media/findux/DATA/Documents/Malta_II/surveys/2022-05-03_Ramla/output_new.mp4"
    weights = "/media/findux/DATA/Documents/Malta_II/results/7050_2022-07-22_175457/train/exp/weights/7050_best.pt"

    drone = "M2EA"
    sensor_width = DRONE_MODELS[drone]["sensor_width_mm"]
    focal_len = DRONE_MODELS[drone]["focal_length_real_mm"]
    yolo_root = "/media/findux/DATA/Documents/Malta_II/yolov5/"

    main(fpath_video=video,
         fpath_weights=weights,
         fdir_yolo_repo=yolo_root,
         conf_thresh=0.80,
         use_orig_resolution=True)
