from pathlib import Path

DEFAULT_IMAGE_DIR = Path.home() / "doc_models_imgs"

# TODO make pydantic basesettings and add as Document arg.
ROUNDING_PRECISION = 1
FONT_ROUNDING_PRECISION = 1
BBOX_ROUNDING_PRECISION = 1


# Minimum allowable ratio for each font: word_space_count / max_word_space_count
MIN_WORD_SPACE_COUNT_RATIO = 0.2
# Minimum allowable ratio for each line: line_space_count / max_line_space_count
MIN_LINE_SPACE_COUNT_RATIO = 0.25

MAX_COMMON_WORD_SPACE_DIFF = 0.2

MAX_COMMON_LINE_SPACE_DIFF = 0.1
