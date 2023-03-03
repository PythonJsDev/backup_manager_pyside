import pytest


@pytest.fixture(scope="session")
def test_path_dirs(tmp_path_factory):
    """Creation de l'arborescence 'dir/sub_dir/last_dir'."""
    dir = tmp_path_factory.mktemp("dir", numbered=False) / "sub_dir"
    dir.mkdir()
    sub_dir = dir / "last_dir"
    sub_dir.mkdir()
    return sub_dir


@pytest.fixture(scope="session")
def three_files_in_dir_root(tmp_path_factory):
    """Creation de 3 fichiers dans le dossier 'root'."""
    root = tmp_path_factory.mktemp("root", numbered=False)
    (root / 'file_1.txt').write_text("hello")
    (root / 'file_2.py').write_text("hello python")
    (root / 'file_3.png').write_text("hello png")
    return root
