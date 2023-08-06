from patool_unpack import check_archive_format, get_archive_format
from patool_unpack.util import PatoolError


def is_archive(file_path) -> bool:
    try:
        check_archive_format(*get_archive_format(file_path))
        return True
    except PatoolError:
        return False

