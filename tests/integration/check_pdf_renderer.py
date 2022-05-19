import os

import numpy
import numpy as np
import tqdm

import cv2
from marie.utils.utils import ensure_exists

from marie.renderer.pdf_renderer import PdfRenderer
from marie.renderer.text_renderer import TextRenderer
from marie.boxes.box_processor import PSMode
from marie.boxes.craft_box_processor import BoxProcessorCraft
from marie.boxes.textfusenet_box_processor import BoxProcessorTextFuseNet
from marie.document.craft_icr_processor import CraftIcrProcessor
from marie.document.trocr_icr_processor import TrOcrIcrProcessor

from PIL import Image


def __scale_width(src, target_size, crop_size, method=Image.BICUBIC):
    img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    ow, oh = img.size
    if ow == target_size and oh >= crop_size:
        return img
    w = target_size
    h = int(max(target_size * oh / ow, crop_size))

    pil_image = img.resize((w, h), method)
    open_cv_image = numpy.array(pil_image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1]
    return open_cv_image


# https://stackoverflow.com/questions/23853632/which-kind-of-interpolation-best-for-resizing-image
def __scale_height(img, target_size, crop_size, method=Image.LANCZOS):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)

    ow, oh = img.size
    scale = oh / target_size
    print(scale)
    w = ow / scale
    h = target_size  # int(max(oh / scale, crop_size))
    return img.resize((int(w), int(h)), method)


if __name__ == "__main__":

    work_dir_boxes = ensure_exists("/tmp/boxes")
    work_dir_icr = ensure_exists("/tmp/icr")
    ensure_exists("/tmp/fragments")

    img_path = "./assets/psm/word/0001.png"
    img_path = "./assets/english/Scanned_documents/Picture_029.tif"
    # img_path = './assets/english/Scanned_documents/t2.tif'
    img_path = "./assets/english/Scanned_documents/Picture_010.tif"
    # img_path = "./assets/english/Lines/002.png"
    # img_path = './assets/english/Lines/001.png'
    # img_path = './assets/english/Lines/003.png'
    # img_path = './assets/english/Lines/005.png'
    # img_path = './assets/english/Lines/004.png'

    img_path = "/home/greg/dataset/medprov/PID/150300431/clean/PID_576_7188_0_150300431_page_0005.tif"
    # img_path = "/opt/grapnel/burst/150459314_2_cleaned.tiff"
    # img_path = "/home/gbugaj/data/rms-asp/149495857/clean/PID_576_7188_0_149495857_page_0003.tif"
    # img_path = (
    #     "/home/gbugaj/Downloads/task_training-01-2022_04_26_14_31_23-coco/images/corr-indexing/train/152606114_2.png"
    # )
    # img_path = "/home/gbugaj/dev/corr-routing/corr-document-dump/cache/152606114.tif"
    # img_path = "/home/gbugaj/dev/corr-routing/corr-document-dump/extracted/152613029_3.png"

    # cal_mean_std('./assets/english/Scanned_documents/')

    if not os.path.exists(img_path):
        raise Exception(f"File not found : {img_path}")

    if True:
        key = img_path.split("/")[-1]
        src_img = cv2.imread(img_path)
        image = src_img
        # image = __scale_width(src_img, 2000, 1000)
        # cv2.imwrite("/tmp/resized-2048.png", image)

        box = BoxProcessorCraft(work_dir=work_dir_boxes, models_dir="./model_zoo/craft", cuda=False)
        # box = BoxProcessorTextFuseNet(work_dir=work_dir_boxes, models_dir='./models/fusenet', cuda=False)
        icr = TrOcrIcrProcessor(work_dir=work_dir_icr, cuda=False)
        # icr = CraftIcrProcessor(work_dir=work_dir_icr, cuda=False)

        boxes, img_fragments, lines, _ = box.extract_bounding_boxes(key, "field", image, PSMode.SPARSE)
        result, overlay_image = icr.recognize(key, "test", image, boxes, img_fragments, lines)

        output_filename = "/tmp/result-2048-craf-lines.pdf"
        print("Testing pdf render")

        renderer = PdfRenderer(config={"preserve_interword_spaces": True})
        renderer.render(image, result, output_filename)