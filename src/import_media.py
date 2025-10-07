import logging
import os

from argparse import Namespace


from utility.db_util import validate_database_path
from utility.find_media import find_media_files_iterator


def import_command(args: Namespace) -> None:
    logging.debug(f"Running import media command with args: {args}")
    import_media(args.database_path, args.media_folders)


def import_media(db_path: str, media_folders: list[str]) -> None:
    validate_database_path(db_path)
    picture_counter = 0
    video_counter = 0
    for folder in media_folders:
        if not os.path.exists(folder):
            logging.warning(f"Media folder does not exist: {folder}")
            continue
        for batch in find_media_files_iterator(folder):
            for media in batch:
                if media.is_image():
                    picture_counter += 1
                else:
                    video_counter += 1
            logging.debug(f"Processed a batch of {len(batch)} media files")

    logging.info(f"Total images: {picture_counter}, Total videos: {video_counter}")
