from pathlib import Path

import click
import cv2
from doc_models.components import Document
from doc_models.visualization import img_draw
from doc_models.visualization.colors import BGRColors
from doc_models.visualization.drawer import ImgDraw
from doc_models.visualization.types import Font

img_base_dir = "/home/dan/my-github-packages/pdf-extract/aapl10k_images"
pdf_file = "/home/dan/my-github-packages/pdf-extract/tests/data/aapl10k.pdf"

doc = Document(pdf_file, ocr_engines=None)
draw = ImgDraw(
    doc=doc,
    img_base_dir=img_base_dir,
)
draw.line_clusters(pg_idx=3, color=BGRColors.RED, thickness=4)
