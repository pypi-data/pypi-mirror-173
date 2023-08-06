from datetime import datetime
from pathlib import Path
from statistics import mean, stdev
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

import cv2
from doc_models import logger
from doc_models.components.document import Document
from doc_models.images.core import ImgMgr
from doc_models.types import BBox, FilePath
from tqdm import tqdm

from .colors import BGRColors, Color, next_color
from .text import _text_row_bboxes
from .types import Font, PageImg
from .utils import img_space_bbox, pad_image


class ImgDraw:
    """Draw shapes and text on document page images."""

    def __init__(
        self, doc: Document, img_base_dir: FilePath, default_font: Optional[Font] = None
    ) -> None:
        """
        Args:
            doc (Document): The document who's pages should be drawn on.
            img_base_dir (FilePath): Base directory where image folders should be created.

        TODO add legend option.
        """
        self.doc = doc
        self.img_base_dir = Path(img_base_dir)
        self.default_font = default_font or Font()
        self.img_mgr = ImgMgr(
            file=doc.file, n_pages=len(doc.pages), save_dir=self.img_base_dir
        )
        # map page index to page image.
        self._pg_imgs = {p.index: PageImg(page=p) for p in self.doc.pages}

    def add_text(
        self,
        pg: Union[int, PageImg],
        text: Union[Dict[str, Any], str, Sequence[str]],
        bbox: BBox,
        bbox_img_space: bool = False,
        text_outside_bbox: bool = True,
        text_loc: Literal["left", "right", "center"] = "left",
        text_align: Literal["left", "right", "center"] = "left",
        offset: int = 0,
        color: Optional[Color] = None,
        font: Optional[Font] = None,
    ):
        """Draw text on document page images.

        Args:
            pg_img (PageImg): _description_
            text (Union[Dict[str, Any], str, Sequence[str]]): _description_
            font (Optional[Font]): _description_
            bbox (BBox): _description_
            bbox_img_space (bool, optional): _description_. Defaults to False.
            text_outside_bbox (bool, optional): _description_. Defaults to True.
            text_loc (Literal[&quot;left&quot;, &quot;right&quot;, &quot;center&quot;], optional): _description_. Defaults to "left".
            text_align (Literal[&quot;left&quot;, &quot;right&quot;, &quot;center&quot;], optional): _description_. Defaults to "left".
            offset (int, optional): _description_. Defaults to 0.
            color (Optional[Color], optional): _description_. Defaults to None.
        """
        pg_img = self.get_page_imgs(pg) if isinstance(pg, int) else pg
        font = font or self.default_font
        if not bbox_img_space:
            bbox = img_space_bbox(pg_img, bbox)
        rows_width, _, rows_bbox_data = _text_row_bboxes(
            text=text,
            outer_bbox=bbox,
            font=font,
        )
        # compute the bounds around the group of text rows and add padding to the image if text extends beyond current image size.
        if text_loc == "left":
            if text_outside_bbox:
                text_left_bound = bbox.left - rows_width - offset
                text_right_bound = bbox.left - offset
            else:
                text_left_bound = bbox.left + offset
                text_right_bound = bbox.left + rows_width + offset
            # add padding if needed.
            if text_left_bound < 0:
                padding_size = -1 * text_left_bound
                pad_image(img=pg_img.img, padding_size=padding_size, padding_dir="left")
                # shift coordinates to adjust for padding.
                text_left_bound = 0
                text_right_bound += padding_size
        elif text_loc == "right":
            text_left_bound = bbox.right + offset
            text_right_bound = text_left_bound + rows_width
            if text_right_bound > pg_img.page.right:
                pad_image(
                    img=pg_img.img,
                    padding_size=text_right_bound - pg_img.page.right,
                    padding_dir="right",
                )
            # TODO finish this.
        elif text_loc == "center":
            # TODO finish this.
            pass
        text_center = round((text_right_bound - text_left_bound) / 2)
        # draw all text rows in image.
        for txt_data in rows_bbox_data:
            if text_align == "right":
                x_pos = text_right_bound - txt_data.width
            elif text_align == "left":
                x_pos = text_left_bound
            elif text_align == "center":
                x_pos = text_center - (txt_data.width / 2)
            # all rows within column have same right position.
            cv2.putText(
                img=pg_img.img,
                text=txt_data.text,
                org=(x_pos, txt_data.bottom),
                fontFace=font.font_face,
                fontScale=font.font_scale,
                thickness=font.thickness,
                lineType=font.line_type,
                color=color or next_color(),
            )

    def lines(
        self,
        pg_idx: Optional[int] = None,
        line_num_loc: Optional[Literal["left", "right", "center"]] = "left",
        thickness: int = 2,
        color: Color = BGRColors.BLUE,
    ):
        """Draw lines on an image, optionally with line numbers.

        Args:
            pg_idx (Optional[int], optional): Index of the page to draw on. If None, all pages will be used.
            line_num_loc (Optional[Literal["left", "right", "center"]], optional): Where to place line numbers. Defaults to "left".
            color (Optional[Color], optional): Color to use to for bounding boxes and text. Defaults to None.
        """

        for pg_img in tqdm(self.get_page_imgs(pg_idx)):
            for line in pg_img.page.lines:
                self.rectangle(
                    pg_img=pg_img,
                    bbox=line.bbox,
                    color=color,
                    thickness=thickness,
                )
                if line_num_loc:
                    self.add_text(
                        pg=pg_img,
                        bbox=line.bbox,
                        text=line.y_index,
                        text_loc=line_num_loc,
                        color=color,
                    )
            pg_img.ft_names.add("Lines")

    def line_segs(
        self,
        pg_idx: Optional[int] = None,
        thickness: int = 2,
        color: Color = BGRColors.GREEN,
    ):
        """Draw line segments.

        Args:
            pg_idx (Optional[int], optional): Index of the page to draw on. If None, all pages will be used.
            color (Optional[Color], optional): Color to use to for bounding boxes and text. Defaults to None.
        """

        for pg_img in tqdm(self.get_page_imgs(pg_idx)):
            for line in pg_img.page.lines:
                for seg in line.members:
                    self.rectangle(
                        pg_img=pg_img,
                        bbox=seg.bbox,
                        color=color,
                        thickness=thickness,
                    )
            pg_img.ft_names.add("LineSegs")

    def line_clusters(
        self,
        pg_idx=None,
        thickness: int = 2,
        color=BGRColors.RED,
    ):
        """Draw bounding box around a cluster."""
        for pg_img in self.get_page_imgs(pg_idx):
            for cluster in pg_img.page.line_clusters:
                members_wsb = [m.whitespace_below for m in cluster.members]
                n_is_exp_line_space = len(
                    [
                        line
                        for prev_idx, line in enumerate(cluster.members[1:])
                        if self.doc.line_spacing.is_expected_line_space(
                            cluster.members[prev_idx], line
                        )
                    ]
                )
                txt_data = {
                    "wsb-mean": mean(members_wsb),
                    "wsb-stdev": stdev(members_wsb),
                    "exp-line-space": f"{n_is_exp_line_space}/{len(cluster.members)-1}",
                }
                self.add_text(pg=pg_img, text=txt_data, bbox=cluster.bbox, color=color)
                self.rectangle(
                    pg_img=pg_img,
                    bbox=cluster.bbox,
                    color=color,
                    thickness=thickness,
                )
            pg_img.ft_names.add("LineClust")

    def cluster_cells():
        pass

    def expected_line_space(self, pg_idx: Optional[int] = None):
        for pg_img in tqdm(self.get_page_imgs(pg_idx)):
            for prev_idx, line in enumerate(pg_img.page.lines[1:]):
                prev_line = pg_img.page.lines[prev_idx]
                color = (
                    BGRColors.GREEN
                    if self.doc.line_spacing.is_expected_line_space(
                        upper_line=prev_line, lower_line=line
                    )
                    else BGRColors.RED
                )
                self.rectangle(
                    pg_img=pg_img,
                    color=color,
                    thickness=-1,
                    bbox=BBox(
                        top=prev_line.bbox.bottom,
                        bottom=line.bbox.top,
                        left=min([prev_line.bbox.left, line.bbox.left]),
                        right=max([prev_line.bbox.right, line.bbox.right]),
                    ),
                )
            pg_img.ft_names.add("ExpLineSpace")

    def rectangle(
        self,
        pg_img: PageImg,
        bbox: BBox,
        bbox_img_space: bool = False,
        thickness: int = 2,
        color: Optional[Color] = None,
        line_type: int = cv2.LINE_8,
    ):
        """Draw a rectangle on a page image.

        Args:
            pg_img (PageImg): The page to draw on.
            bbox (BBox): Bounding box of the rectangle to draw.
            bbox_img_space (bool, optional): Whether the bounding box is in image coordinates or PDF coordinates. Defaults to False.
            thickness (int): Thickness to draw bbox. Defaults to 1.
            color (Optional[Color], optional): Color of the rectangle. If None, a random color will be used. Defaults to None.
            line_type (int): Line type used to draw bbox (This really does not matter. They all look the same). Defaults to cv2.LINE_8. Options: FILLED, LINE_4 (4-connected line), LINE_8 (8-connected line), LINE_AA (antialiased line)
        """
        if not bbox_img_space:
            bbox = img_space_bbox(pg_img, bbox)
        cv2.rectangle(
            img=pg_img.img,
            pt1=(bbox.left, bbox.top),
            pt2=(bbox.right, bbox.bottom),
            color=color or next_color(),
            thickness=thickness,
            lineType=line_type,
        )

    def save(
        self,
        save_dir: Optional[FilePath] = None,
    ) -> List[Path]:
        """Save drawing images to jpg files.

        Args:
            save_dir (Optional[FilePath], optional): Base directory where image folders should be placed.
            If None, a directory of directories will be generate.
            For each image with drawn features (as specified in the `PageImg` `ft_names` attribute),
            the save folder format will be the names of the drawn features joined with underscores (_).
            Images with no drawing features will be save to a folder with with current time (`_page_imgs_%Y%m%dT%H%M%S`)

        Returns:
            List[Path]: Paths to the saved image files.
        """
        now = datetime.now().strftime("%Y%m%dT%H%M%S")
        file_paths = []
        for pg_img in self._pg_imgs.values():
            if pg_img.img is not None:
                if save_dir is None:
                    save_dir = self.img_base_dir.joinpath(
                        "_".join(sorted(pg_img.ft_names)) or f"_page_imgs_{now}"
                    )
                save_dir.mkdir(exist_ok=True, parents=True)
                save_path = save_dir / self.img_mgr.image_file_name(pg_img.page.index)
                cv2.imwrite(str(save_path), pg_img.img)
                file_paths.append(save_path)
        logger.info(
            "Saved drawing images to: %s",
            ",\n".join({str(p.parent) for p in file_paths}),
        )
        return file_paths

    def get_page_imgs(self, pg_idx: Optional[int] = None) -> List[PageImg]:
        """Get images of pages.

        Args:
            pg_idx (Optional[int], optional): Index of the page to get. In None, all page indexes will be used. Defaults to None.

        Returns:
            List[PageImg]: The Page images.
        """
        pg_idxs = [p.index for p in self.doc.pages] if pg_idx is None else [pg_idx]
        for pg_idx in pg_idxs:
            # load the image if it is not already cached.
            if self._pg_imgs[pg_idx].img is None:
                self._pg_imgs[pg_idx].img = self.img_mgr.get_page_image(pg_idx)
        return [self._pg_imgs[idx] for idx in pg_idxs]


def img_draw(pdf_file: FilePath, img_base_dir: FilePath):
    doc = Document(pdf_file)
    font = Font(
        font_face=cv2.FONT_HERSHEY_SIMPLEX,
        font_scale=1,
        thickness=2,
    )
    draw = ImgDraw(
        doc=doc,
        font=font,
        img_base_dir=img_base_dir,
    )
    draw.lines(color=BGRColors.BLUE)
    draw.line_segs(color=BGRColors.GREEN)
    draw.save()
