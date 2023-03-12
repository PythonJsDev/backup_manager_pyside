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


@pytest.fixture(scope="session")
def tree_structure_src(tmp_path_factory):
    """création de l'arborescence:
    root/dir_a/hello.txt
    root/dir_b/
    root/python.py
    root/dir_c/hello_in_dir_c.txt
    root/dir_c/another_hello_in_dir_c.txt
    root/dir_c/sub_dir_c
    """
    root = tmp_path_factory.mktemp("root")
    dir_a = root / 'dir_a'
    dir_a.mkdir()
    (dir_a / 'hello.txt').write_text("hello")

    (root / 'dir_b').mkdir()

    (root / 'python.py').write_text("hello python")

    dir_c = root / 'dir_c'
    dir_c.mkdir()
    (dir_c / 'hello_in_dir_c.txt').write_text("hello in the directory c")
    (dir_c / 'another_hello_in_dir_c.txt').write_text("another hello in dir c")
    (dir_c / 'sub_dir_c').mkdir()
    return root


@pytest.fixture(scope="session")
def tree_structure_target(tmp_path_factory):
    """création de l'arborescence:
    root/dir_a/hello.txt
    root/dir_d/
    root/javascript.js
    root/dir_e/sub_dir_e
    """
    root = tmp_path_factory.mktemp("root")
    dir_a = root / 'dir_a'
    dir_a.mkdir()
    (dir_a / 'hello.txt').write_text("hello")

    (root / 'dir_d').mkdir()

    (root / 'javascript.js').write_text("hello javascript")

    dir_e = root / 'dir_e'
    dir_e.mkdir()
    (dir_e / 'sub_dir_e').mkdir()
    return root
