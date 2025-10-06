import os
import re
from collections.abc import Callable
from data_types import FileNameData


def _extract_px(filename: str) -> FileNameData:
    parts = filename.split("_")
    if len(parts) < 2:
        raise ValueError(f"Unexpected filename format: {filename}")
    date = parts[1]
    order = parts[2] if len(parts) > 2 else "0"
    return date, order, "phone"


def _extract_wa(filename: str) -> FileNameData:
    parts = filename.split("-")
    if len(parts) < 2:
        raise ValueError(f"Unexpected filename format: {filename}")
    date = parts[1]
    order = parts[2].replace("WA", "") if len(parts) > 2 else "0"
    return date, order, "whatsapp"


def _extract_generic(filename: str) -> FileNameData:
    parts = filename.split("_")
    if len(parts) < 2:
        raise ValueError(f"Unexpected filename format: {filename}")
    date = parts[0]
    order = parts[1][:6] if len(parts) > 1 else "0"
    return date, order, "phone"


# (pattern, extraction function)
PATTERNS: list[tuple[str, Callable[[str], FileNameData]]] = [
    (r"^PXL_\d{8}_\d{9}", _extract_px),
    (r"^(VID|IMG)-\d{8}-WA\d{4}", _extract_wa),
    (r"^\d{8}_\d{6}", _extract_generic),
]


def extract_data_from_filename(filename: str) -> tuple[str, str, str]:
    """
    Extracts the date, sequence/order number, and origin from a media filename.

    Parameters
    ----------
    filename : str
        The path to the media file.

    Returns
    -------
    tuple[str, str, str]
        A tuple containing:
          - date (str): Date in ISO format (YYYY-MM-DD), or "0000-00-00" if unknown.
          - order (str): A numeric sequence or identifier string.
          - source (str): One of {"phone", "whatsapp", "unknown"}.
    """

    base_name = os.path.splitext(os.path.basename(filename))[0]
    date, order, origin = "0", "0", "unknown"
    for pattern, extractor in PATTERNS:
        if re.match(pattern, base_name, re.IGNORECASE):
            date, order, origin = extractor(base_name)
            break
    else:
        raise ValueError(f"Filename '{filename}' does not match expected patterns")

    date = f"{date[:4]}-{date[4:6]}-{date[6:]}" if len(date) == 8 else "0000-00-00"
    return date, order, origin
