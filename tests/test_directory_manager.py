from pathlib import Path
from unittest.mock import Mock, call

from backup_manager_pyside.models.directory_manager import DirectoryManager


def test_get_last_folder_without_file(test_path_dirs):
    """Vérifie que 'get_last_folder' retourne le dernier dossier d'un chemin"""
    assert DirectoryManager().get_last_folder(test_path_dirs) == "last_dir"


def test_get_last_folder_with_file(test_path_dirs):
    """Vérifie que 'get_last_folder' retourne le dernier dossier d'un chemin"""
    assert (
        DirectoryManager().get_last_folder(test_path_dirs / "hello.txt")
        == "last_dir"
    )


def test_get_subdirectories_with_empty_folders(tmp_path):
    """Vérifie que get_subdirectories retourne la liste des sous-dossiers vides
    contenu dans le dossier root"""
    root = tmp_path / 'root'
    root.mkdir()
    (root / 'dir_a').mkdir()
    (root / 'dir_b').mkdir()
    (root / 'dir_c').mkdir()
    assert DirectoryManager().get_subdirectories(root) == [
        Path('dir_a'),
        Path('dir_b'),
        Path('dir_c'),
    ]


def test_get_subdirectories_with_not_empty_folders(tmp_path):
    """Vérifie que get_subdirectories retourne la liste des sous-dossiers
    contenu dans le dossier root:
    root/dir_a/hello.txt
    root/dir_b/
    root/pyton.py
    root/dir_c/sub_dir_c
    """
    root = tmp_path / 'root'
    root.mkdir()
    dir_a = root / 'dir_a'
    dir_a.mkdir()
    (dir_a / 'hello.txt').write_text("hello")

    (root / 'dir_b').mkdir()

    (root / 'python.py').write_text("hello python")

    dir_c = root / 'dir_c'
    dir_c.mkdir()
    (dir_c / 'sub_dir_c').mkdir()

    assert DirectoryManager().get_subdirectories(root) == [
        Path('dir_a'),
        Path('dir_b'),
        Path('dir_c'),
        Path('dir_c/sub_dir_c'),
    ]


def test_diff_between_two_folder_lists():
    """Vérifie que diff_between_two_folder_lists retourne les dossiers de
    list_1 manquants à list_2 et les dossiers de list_2 manquants à list_1"""
    list_1 = [
        Path('dir_a'),
        Path('dir_b'),
        Path('dir_c'),
        Path('dir_d'),
    ]
    list_2 = [
        Path('dir_a'),
        Path('dir_x'),
        Path('dir_y'),
    ]
    expected_missing_in_list_2 = [Path('dir_b'), Path('dir_c'), Path('dir_d')]
    expected_missing_in_list_1 = [Path('dir_x'), Path('dir_y')]
    (
        missing_in_list_2,
        missing_in_list_1,
    ) = DirectoryManager().diff_between_two_folder_lists(list_1, list_2)

    assert sorted(missing_in_list_2) == sorted(expected_missing_in_list_2)
    assert sorted(missing_in_list_1) == sorted(expected_missing_in_list_1)


def test_create_folders(tmp_path):
    """Teste la création de la liste de dossiers 'folders' dans un dossier
    temporaire."""
    folders = ["dir_A", "dir_B", "dir_C"]
    DirectoryManager().create_folders(tmp_path, folders)
    get_folders = [f.name for f in tmp_path.iterdir() if f.is_dir()]
    assert folders.sort() == get_folders.sort()


def test_create_folders_OSError(monkeypatch):
    """Verifie que si, lors de la création d'un dossier, une execption OSError
    est le levée, celle-ci est gérée."""
    folders = ["dir_A"]
    path_target = Path(r'Z:\backup')
    mock_mkdir = Mock()
    monkeypatch.setattr(
        "backup_manager_pyside.models.directory_manager.Path.mkdir", mock_mkdir
    )
    mock_mkdir.side_effect = OSError('error message')
    mock_error_msg = Mock()
    monkeypatch.setattr(
        "backup_manager_pyside.models.directory_manager.Message.error_msg",
        mock_error_msg,
    )
    error_msg = "Une erreur s'est produite !! : error message"

    DirectoryManager().create_folders(path_target, folders)
    mock_error_msg.assert_called_once_with(error_msg)


def test_delete_folders_call_shutil(monkeypatch):
    """Verifie que la fonction shutil.rmtree soit appelé le bon nombre de fois
    avec les bons arguments"""
    folders_tree = [
        r"Z:\backup\root_target\dirname_A",
        r"Z:\backup\root_target\dirname_B\sub_dirname_B",
    ]
    path_target = Path(r'Z:\backup')
    mock_shutil = Mock()
    monkeypatch.setattr(
        "backup_manager_pyside.models.directory_manager.shutil", mock_shutil
    )
    DirectoryManager().delete_folders(path_target, folders_tree)
    expected_calls = [
        call(Path(folders_tree[0])),
        call(Path(folders_tree[1])),
    ]
    for called, expected_call in zip(
        mock_shutil.rmtree.mock_calls, expected_calls
    ):
        assert called == expected_call


def test_delete_folders_OSError(monkeypatch):
    """Verifie que si shutil.rmtree lève une exception OSError,
    celle-ci est gérée."""
    folders_tree = [
        r"Z:\backup\root_target\dirname_A",
    ]
    path_target = Path(r'Z:\backup')
    mock_shutil = Mock()
    monkeypatch.setattr(
        "backup_manager_pyside.models.directory_manager.shutil", mock_shutil
    )
    mock_shutil.rmtree.side_effect = OSError('error message')
    mock_error_msg = Mock()
    monkeypatch.setattr(
        "backup_manager_pyside.models.directory_manager.Message.error_msg",
        mock_error_msg,
    )
    error_msg = "Une erreur s'est produite !! : error message"

    DirectoryManager().delete_folders(path_target, folders_tree)
    mock_error_msg.assert_called_once_with(error_msg)
