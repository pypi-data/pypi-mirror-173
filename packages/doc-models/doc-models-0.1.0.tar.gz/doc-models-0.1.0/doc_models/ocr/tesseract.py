from collections import defaultdict
from typing import Dict, List
from xml.dom.minidom import Document

import cv2
import pytesseract
from doc_models.components import Cluster, Word
from doc_models.types import BBox
from doc_models.utils import WriteOnceDict
from pytesseract import Output


class TesseractData:
    words: List[Word]
    lines: List[Cluster]
    blocks: List[Cluster]
    paragraphs: List[Cluster]
    line_bbox: Dict[int, BBox]
    block_bbox: Dict[int, BBox]
    para_bbox: Dict[int, BBox]
    doc: Document


def tesseract_data(img_file: str):
    # TODO np.array arg
    img = cv2.imread(str(img_file))
    # TODO filter.
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    fields = [
        "level",
        "page_num",
        "block_num",
        "par_num",
        "line_num",
        "left",
        "top",
        "width",
        "height",
        "conf",
        "text",
    ]
    data = [dict(zip(fields, row)) for row in zip(*[data[f] for f in fields])]
    # line words.
    lines = defaultdict(list)
    # line numbers
    paras, blocks = defaultdict(set), defaultdict(set)
    page_bbox = WriteOnceDict()
    line_bbox = WriteOnceDict()
    block_bbox = WriteOnceDict()
    para_bbox = WriteOnceDict()

    words = []
    # levels: 1 - page, 2 - block, 3 - para, 4 - line,  5 - word
    for d in data:
        line_num = d["line_num"]
        # level 5 == word
        if (level := d["level"]) == 5:
            word = Word(
                text=d["text"],
                confidence=d["conf"],
                top=d["top"],
                left=d["left"],
                width=d["width"],
                height=d["height"],
            )
            words.append(word)
            # first actual index is 1. 0 is used for features that aren't the feature.
            lines[line_num].append(word)
        # level 4 == line
        elif level == 4:
            line_bbox[line_num] = BBox(
                top=d["top"],
                left=d["left"],
                width=d["width"],
                height=d["height"],
            )
            paras[d["par_num"]].add(line_num)
            blocks[d["block_num"]].add(line_num)
        # level 3 == paragraph
        elif level == 3:
            para_bbox[d["para_num"]] = BBox(
                top=d["top"],
                left=d["left"],
                width=d["width"],
                height=d["height"],
            )
        # level 2 == block
        elif level == 2:
            block_bbox[d["block_num"]] = BBox(
                top=d["top"],
                left=d["left"],
                width=d["width"],
                height=d["height"],
            )
        elif level == 1:
            page_bbox[d["page_bbox"]] = BBox(
                top=d["top"],
                left=d["left"],
                width=d["width"],
                height=d["height"],
            )

        # TODO convert to pdf coordinrates with level 1 box
