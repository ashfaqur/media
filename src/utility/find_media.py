import logging
import os
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Generator

from data_types import MediaData
from utility.filename_util import extract_data_from_filename


# Normalize all keys to lowercase
EXTENSION_TO_TYPE = {
    ext.lower(): typ
    for ext, typ in {
        ".jpg": "image",
        ".jpeg": "image",
        ".png": "image",
        ".mp4": "video",
        ".mov": "video",
        ".avi": "video",
    }.items()
}


@dataclass
class MediaMetaData:
    date: str
    path: str
    media_type: str
    order: str
    origin: str
    size: int

    def is_image(self) -> bool:
        return self.media_type == "image"

    def get_data(self) -> MediaData:
        return self.date, self.path, self.media_type, self.order, self.origin, self.size

    def __str__(self) -> str:
        return (
            f"MediaMetaData("
            f"date={self.date}, "
            f"path={self.path}, "
            f"media_type={self.media_type}, "
            f"order={self.order}, "
            f"origin={self.origin}, "
            f"size={self.size})"
        )


def find_media_files_iterator(
    folder_path: str, batch_size: int = 1000
) -> Generator[list[MediaData], None, None]:
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
    batch: list[MediaData] = []

    video_counter = 0
    picture_counter = 0
    skipped_files = 0
    total_size = 0

    for file_path in folder.rglob("*"):
        if not file_path.is_file():
            continue

        ext = file_path.suffix.lower()
        media_type = EXTENSION_TO_TYPE.get(ext)
        if not media_type:
            continue
        date, order, origin = "0", "0", "unknown"
        try:
            date, order, origin = extract_data_from_filename(file_path.name)
        except ValueError as e:
            logging.debug(f"Skipping file '{file_path}': {e}")
            skipped_files += 1
            continue
        if not date:
            date = get_file_mod_date(file_path)
            logging.debug(
                f"Date not found in filename {file_path}, using file mod date: {date}"
            )
        if not date:
            logging.warning(f"Skipping file '{file_path}': date not found")
            skipped_files += 1
            continue
        size = file_path.stat().st_size
        data = MediaMetaData(
            date=date,
            path=str(file_path),
            media_type=media_type,
            order=order,
            origin=origin,
            size=size,
        )
        if media_type == "video":
            video_counter += 1
        else:
            picture_counter += 1
        total_size += size
        logging.debug(f"Found media file: {data}")
        batch.append(data.get_data())

        if len(batch) >= batch_size:
            yield batch
            batch = []

    # Yield any remaining files
    if batch:
        yield batch

    logging.info(f"Found {video_counter} videos and {picture_counter} pictures")
    logging.info(f"Skipped {skipped_files} files")
    logging.debug(
        f"Total size of media files: {total_size / 1024 / 1024 / 1024:.2f} GB"
    )


def get_file_mod_date(filepath: Path) -> str:
    ts = os.path.getmtime(filepath.absolute())
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
