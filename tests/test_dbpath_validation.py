import pytest
from pytest_mock import MockerFixture

from utility.db_util import validate_database_path


def test_existing_db_path(mocker: MockerFixture) -> None:
    mock_path = mocker.patch("utility.db_util.Path").return_value
    mock_path.suffix = ".db"
    mock_path.parent.exists.return_value = True
    mock_path.is_file.return_value = True

    assert validate_database_path("fake/path/test.db") is True


def test_invalid_extension(mocker: MockerFixture) -> None:
    mock_path = mocker.patch("utility.db_util.Path").return_value
    mock_path.suffix = ".txt"

    with pytest.raises(ValueError, match="Invalid database path"):
        validate_database_path("fake/path/file.txt")


def test_new_db_path(mocker: MockerFixture) -> None:
    mock_path = mocker.patch("utility.db_util.Path").return_value
    mock_path.suffix = ".db"
    mock_path.parent.exists.return_value = True
    mock_path.is_file.return_value = False  # simulate new file

    assert validate_database_path("fake/path/new.db") is False


def test_missing_folder(mocker: MockerFixture) -> None:
    mock_path = mocker.patch("utility.db_util.Path").return_value
    mock_path.suffix = ".db"
    mock_path.parent.exists.return_value = False

    with pytest.raises(ValueError, match="folder directory does not exist"):
        validate_database_path("fake/path/test.db")
