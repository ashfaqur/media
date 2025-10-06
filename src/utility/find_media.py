import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Generator, List

from utility.filename_util import extract_data_from_filename

EXTENSION_TO_TYPE = {
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".mp4": "video",
    ".mov": "video",
    ".avi": "video",
}


@dataclass
class MediaData:
    date: str
    path: str
    media_type: str
    order: str
    origin: str

    def is_image(self) -> bool:
        return self.media_type == "image"


def find_media_files_iterator(
    folder_path: str, batch_size: int = 1000
) -> Generator[List[MediaData], None, None]:
    """
    Iterate over media files in folder and yield batches of MediaData.

    Parameters
    ----------
    folder_path : str
        Path to folder containing media files.
    batch_size : int
        Override default number of media files per batch.

    Yields
    ------
    List[MediaData]
        A list of MediaData objects of length up to batch_size.
    """
    folder = Path(folder_path)
    batch: List[MediaData] = []

    for file_path in folder.rglob("*"):
        if not file_path.is_file():
            continue

        ext = file_path.suffix.lower()
        media_type = EXTENSION_TO_TYPE.get(ext)
        if not media_type:
            continue

        try:
            date, order, origin = extract_data_from_filename(file_path.name)
        except ValueError as e:
            logging.warning(f"Skipping file '{file_path}': {e}")
            continue
        batch.append(
            MediaData(
                date=date,
                path=str(file_path),
                media_type=media_type,
                order=order,
                origin=origin,
            )
        )

        if len(batch) >= batch_size:
            yield batch
            batch = []

    # Yield any remaining files
    if batch:
        yield batch
