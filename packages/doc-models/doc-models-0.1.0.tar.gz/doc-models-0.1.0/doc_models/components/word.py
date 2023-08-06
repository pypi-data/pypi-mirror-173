import re
from typing import Optional

from doc_models.types import BBox
from poppler.page import TextBox
from unidecode import unidecode


class Word:
    _numeric_re = re.compile(r"[\d$%][\d,.:-]+")
    _uppercase_re = re.compile(r"""^[A-Z.?!-'"()*]+$""")
    _capitalized_re = re.compile(r"^[A-Z]")
    _italic_re = re.compile(r"(?i)italic")
    _bold_re = re.compile(r"(?i)bold")

    def __init__(
        self,
        text: str,
        confidence: int,
        font_name: Optional[str] = None,
        font_size: Optional[float] = None,
        index: Optional[int] = None,
        **bbox_kwargs,
    ) -> None:
        """_summary_

        Args:
            text (str): _description_
            confidence (int): 0-100 value representing confidence that word was correctly recognized. For poppler this will always be 100. For OCR it will likely be less.
            top (int): _description_
            bottom (int): _description_
            left (int): _description_
            right (int): _description_
            font_name (Optional[str], optional): _description_. Defaults to None.
            font_size (Optional[float], optional): _description_. Defaults to None.
            index (Optional[int], optional): _description_. Defaults to None.
        """
        self.text = unidecode(text)
        self.confidence = confidence
        self.bbox = BBox(**bbox_kwargs)
        self.font_name = font_name
        self.font_size = font_size
        # index of where this word is within the document.
        self.index = index
        self.is_bold = (
            self.font_name and self._bold_re.search(self.font_name) is not None
        )
        self.is_italic = (
            self.font_name and self._italic_re.search(self.font_name) is not None
        )
        self.is_capitalized = bool(self._capitalized_re.match(self.text))
        self.is_uppercase = bool(self._uppercase_re.match(self.text))
        self.is_numeric = self._numeric_re.search(self.text) is not None

    @classmethod
    def from_poppler(cls, txt_box: TextBox):
        """Create Word from a poppler TextBox.

        Args:
            txt_box (TextBox): text box containing word data.
        """
        return cls(
            text=txt_box.text,
            confidence=100,
            top=txt_box.bbox.top,
            bottom=txt_box.bbox.bottom,
            left=txt_box.bbox.left,
            right=txt_box.bbox.right,
            font_name=txt_box.get_font_name(),
            font_size=txt_box.get_font_size(),
        )

    def __repr__(self) -> str:
        return f"Word('{self.text}', {self.bbox})"
