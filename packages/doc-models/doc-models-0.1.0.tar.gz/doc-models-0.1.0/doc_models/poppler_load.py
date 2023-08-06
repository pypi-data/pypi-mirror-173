"""Parse PDFs with poppler."""

import multiprocessing as mp
import os
from typing import List, Tuple

import poppler

from doc_models.components.page import load_page_line_words
from doc_models.components.word import Word
from doc_models.types import BBox, FilePath


def load_poppler_doc(file: FilePath) -> List[Tuple[BBox, List[List[Word]]]]:
    global pdoc
    pdoc = poppler.load_from_file(file)
    pg_nums = list(range(pdoc.pages))
    if (n_pg := len(pg_nums)) > 1:
        with mp.Pool(min(n_pg, os.cpu_count())) as p:
            return p.map(load_poppler_page, pg_nums)
    return [load_poppler_page(0)]


def load_poppler_page(index: int) -> Tuple[BBox, List[List[Word]]]:
    pop_page = pdoc.create_page(index)
    lines = load_page_line_words([Word.from_poppler(t) for t in pop_page.text_list(1)])
    pop_bbox = pop_page.page_rect()
    bbox = BBox(
        top=pop_bbox.top,
        bottom=pop_bbox.bottom,
        left=pop_bbox.left,
        right=pop_bbox.right,
    )
    return bbox, lines
