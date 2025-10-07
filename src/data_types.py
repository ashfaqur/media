from typing import TypeAlias

# date, file_path, type, sequence/order, origin, size
MediaData: TypeAlias = tuple[str, str, str, str, str, int]

FileNameData: TypeAlias = tuple[str, str, str]
