from detectron2.data import build_detection_test_loader
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.utils.visualizer import ColorMode
from detectron2.engine import DefaultTrainer

from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.structures import BoxMode
from detectron2 import model_zoo

from detectron2.utils.logger import setup_logger
import detectron2

from lxml.html import fromstring
import torchvision
import torch
import numpy as np
import cv2

from pathlib import Path
import random
import json
import os


# Some basic setup -- setup detectron2 logger
setup_logger()


def dict_from_pascal_voc(file, image_id):
    print(f"Creating image dict from {file} ({image_id})")

    def assert_one(ele_list, is_str=True):
        if len(ele_list) != 1:
            raise Exception(f"Expected a 1 element list: {ele_list}")
        assert len(ele_list) == 1
        if is_str:
            return str(ele_list.pop())
        return ele_list.pop()

    content = Path(file).read_text()
    root = fromstring(content)
    annot = root.xpath("/annotation")
    print(f"ANNOT {annot}")
    annot = assert_one(annot, False)
    return {
        "image_id": image_id,
        "width": assert_one(annot.xpath("./size/width/text()")),
        "height": assert_one(annot.xpath("./size/height/text()")),
        "bbox_mode": BoxMode.XYXY_ABS,
        "annotations": [
            {
                "bbox": [
                    assert_one(obj.xpath("./bndbox/xmin/text()")),
                    assert_one(obj.xpath("./bndbox/ymin/text()")),
                    assert_one(obj.xpath("./bndbox/xmax/text()")),
                    assert_one(obj.xpath("./bndbox/ymax/text()")),
                ],
                "category_id": assert_one(obj.xpath("./name")),
            }
            for obj in annot.xpath("./object")
        ],
    }


def get_img_dicts(label_dir):
    img_dicts = [
        dict_from_pascal_voc(file, idx)
        for idx, file in enumerate(list(label_dir.glob("*.xml")))
    ]
    print(f"Created {len(img_dicts)} image dicts from {img_dicts}")


def get_dataset_name(base_label_dir, op_type):
    assert op_type in ("train", "val")
    return f"{Path(base_label_dir).name}_{op_type}"


def register_img_dicts(base_label_dir):
    for d in ["train", "val"]:
        dataset_name = get_dataset_name(base_label_dir, d)
        print(f"Registering dateset: {dataset_name}")
        DatasetCatalog.register(
            dataset_name, lambda d=d: get_img_dicts(base_label_dir.joinpath(d))
        )
        MetadataCatalog.get(dataset_name).set(
            thing_classes=[
                "chart",
                "chart title",
                "chart subtitle",
                "chart header",
                "chart row",
                "chart row name",
                "chart column",
                "chart column title",
                "chart cell",
            ]
        )


def plot_registered_data_sample(base_label_dir, op_type):
    print(f"Plotting {base_label_dir}, {op_type}")
    dataset_name = get_dataset_name(base_label_dir, op_type)
    metadata = MetadataCatalog.get(dataset_name)
    # verify data is loaded correctly
    dataset_dicts = get_img_dicts(base_label_dir.joinpath(op_type))
    for d in random.sample(dataset_dicts, 3):
        img = cv2.imread(d["file_name"])
        visualizer = Visualizer(img[:, :, ::-1], metadata=metadata, scale=0.5)
        out = visualizer.draw_dataset_dict(d)
        cv2.imshow(out.get_image()[:, :, ::-1])


def get_dataset_cfg():
    # fine-tune a COCO-pretrained R50-FPN Mask R-CNN model
    cfg = get_cfg()
    cfg.merge_from_file(
        model_zoo.get_config_file(
            "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
        )
    )
    cfg.DATASETS.TRAIN = ("balloon_train",)
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
        "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    )  # Let training initialize from model zoo
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
    # 300 iterations seems good enough for this toy dataset; you may need to train longer for a practical dataset
    cfg.SOLVER.MAX_ITER = 300
    # faster, and good enough for this toy dataset (default: 512)
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (ballon)
    return cfg


def train(cfg):
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()


def inference(cfg):
    # run inference with the trained model on the validation dataset.
    # create a predictor using the model we just trained
    # cfg already contains everything we've set previously. Now we changed it a little bit for inference:
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set a custom testing threshold
    predictor = DefaultPredictor(cfg)

    # randomly select several samples to visualize the prediction results.
    dataset_dicts = get_balloon_dicts("balloon/val")
    for d in random.sample(dataset_dicts, 3):
        im = cv2.imread(d["file_name"])
        outputs = predictor(im)
        v = Visualizer(
            im[:, :, ::-1],
            metadata=balloon_metadata,
            scale=0.5,
            # remove the colors of unsegmented pixels. This option is only available for segmentation models
            instance_mode=ColorMode.IMAGE_BW,
        )
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        cv2_imshow(out.get_image()[:, :, ::-1])


def eval_performance():
    # evaluate its performance using AP metric implemented in COCO API.
    evaluator = COCOEvaluator("balloon_val", cfg, False, output_dir="./output/")
    val_loader = build_detection_test_loader(cfg, "balloon_val")
    print(inference_on_dataset(trainer.model, val_loader, evaluator))
