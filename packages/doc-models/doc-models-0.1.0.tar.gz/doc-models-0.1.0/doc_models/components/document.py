from itertools import count
from pathlib import Path
from typing import List, Sequence, Tuple

from doc_models.clustering.spacing import DocLineSpacing, DocWordSpacing
from doc_models.const import DEFAULT_IMAGE_DIR
from doc_models.images import ImgMgr
from doc_models.poppler_load import load_poppler_doc
from doc_models.types import BBox, FilePath, OCREngine

from .cluster import Cluster
from .page import Page
from .word import Word


class Document:
    """A PDF document."""

    def __init__(
        self,
        file: FilePath,
        ocr_engines: Sequence[OCREngine] = ["tesseract"],
        image_dir: Path = DEFAULT_IMAGE_DIR,
    ) -> None:
        """
        Args:
            file (FilePath): Path to PDF file.
            single_proc (bool, optional): Parse the file using a single process. Defaults to False.
        """
        self.file = Path(file)
        self.ocr_engines = ocr_engines
        self.image_dir = image_dir

        # parse the file using poppler.
        doc_contents = load_poppler_doc(self.file)

        self.img_mgr = ImgMgr(
            file=self.file, n_pages=len(doc_contents), save_dir=image_dir
        )
        if ocr_engines:
            # create images if they have not already been created for this document.
            self.img_mgr.create_images(check_exists=True)

        doc_line_words = [
            line_words
            for _, pg_lines_words in doc_contents
            for line_words in pg_lines_words
        ]
        if ocr_engines:
            # extract ocr features.
            pass
        elif not any(l for l in doc_line_words):
            raise RuntimeError(
                "Text could not extracted from PDF and no argument for `ocr_engines` was provided.",
                "Provide an OCR engine name to use OCR to extract text.",
            )
        # set word indexes before constructing DocWordSpacing.
        word_idx = count()
        for line in doc_line_words:
            for word in line:
                word.index = next(word_idx)
        self.word_spacing = DocWordSpacing(doc_line_words)
        self.pages = self._load_pages(doc_contents)
        # set line indexes before constructing DocLineSpacing.
        line_idx = count()
        for page in self.pages:
            for line in page.lines:
                line.y_index = next(line_idx)
        self.line_spacing = DocLineSpacing(self.pages)
        # set page cluster attributes.
        for page in self.pages:
            page.set_clusters(self.line_spacing)

    def _load_pages(
        self, doc_contents: List[Tuple[BBox, List[List[Word]]]]
    ) -> List[Page]:
        pages = []
        for idx, (page_bbox, pg_lines_words) in enumerate(doc_contents):
            lines = [
                Cluster.from_line_words(line_words, self.word_spacing, page_bbox)
                for line_words in pg_lines_words
            ]
            Cluster.set_vertical_whitespace(lines)
            pages.append(Page(index=idx, bbox=page_bbox, lines=lines))
        return pages

    def __repr__(self) -> str:
        return f"Document({self.file.name}, ocr_engines={self.ocr_engines}, image_dir={self.image_dir}. pages={self.pages}"
