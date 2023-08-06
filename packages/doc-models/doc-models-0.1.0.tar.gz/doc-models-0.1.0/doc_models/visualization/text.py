from math import ceil, floor
from typing import Any, Dict, List, Sequence, Tuple, Union

import cv2
from doc_models.types import BBox

from .types import Font, TextBox
from .utils import round_if_float


def _kv_text_rows(text: Dict[str, Any], outer_bbox: BBox, font: Font) -> List[str]:
    rows_data = [
        _get_text_box(f"{k}: {round_if_float(v)}", font) for k, v in text.items()
    ]
    # the height and line space for each row will be the same.
    total_kv_height = sum(r.height + r.line_space for r in rows_data)
    # how many kv pairs do we have to put in each row to fit within outer_bbox?
    kv_per_row = max(1, ceil(total_kv_height / outer_bbox.height))

    n_rows = ceil(len(rows_data) / kv_per_row)

    text_rows = [
        ", ".join([r.text for r in rows_data[i * kv_per_row : (i + 1) * kv_per_row]])
        for i in range(n_rows)
    ]
    return text_rows


def _text_row_bboxes(
    text: Union[Dict[str, Any], str, Sequence[str]],
    outer_bbox: BBox,
    font: Font,
) -> Tuple[float, float, List[TextBox]]:
    """Stack text rows within an outer bounding box.

    Args:
        text (Union[Dict[str, Any], str, Sequence[str]]): The text that should be placed in `outer_bbox`.
        outer_bbox (BBox): The bbox that text should be placed in.

    Returns:
        Tuple[float, float, List[TextBox]]: _description_
    """

    # format text as rows.
    if isinstance(text, dict):
        text_rows = _kv_text_rows(text, outer_bbox, font)
    elif isinstance(text, (str, float)):
        text_rows = [round_if_float(text)]
    elif isinstance(text, int):
        text_rows = [str(text)]
    elif isinstance(text, (list, tuple, set)):
        text_rows = [round_if_float(t) for t in text]
    else:
        raise ValueError(f"Invalid type for text argument ({type(text)}): {text}")

    # get sizes of text lines.
    text_rows = [_get_text_box(line, font) for line in text_rows]
    total_text_height = sum(r.height + r.line_space for r in text_rows)
    # add top and bottom coordinates so that the text rows will be centered in the outer_bbox.
    # TODO add different non-centered text alignments.
    row_top = floor(outer_bbox.y_center - total_text_height / 2)
    for row_text in text_rows:
        row_text.update(
            bottom=row_top + row_text.height,
            top=row_top,
        )
        # top for next row.
        row_top = row_text.bottom + row_text.line_space
    # find width and height of box surrounding all text rows.
    txt_width = max([r.width for r in text_rows])
    # height = bottom row bottom - top row top
    txt_height = text_rows[-1].bottom - text_rows[0].top
    return txt_width, txt_height, text_rows


def _get_text_box(text: str, font: Font) -> TextBox:
    (width, height), baseline = cv2.getTextSize(
        text=text,
        fontFace=font.font_face,
        fontScale=font.font_scale,
        thickness=font.thickness,
    )
    return TextBox(text=text, height=height, width=width, line_space=baseline // 2)
