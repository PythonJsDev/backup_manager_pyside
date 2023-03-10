from pathlib import Path
from unittest.mock import Mock, call

from backup_manager_pyside.models.file_manager import FileManager


def test_get_files_names_sizes(three_files_in_dir_root):
    """Vérifie que 'get_files_names_sizes' retourne un dictionnaire dont les
    clés sont les noms des fichiers et les valeurs sont les tailles du fichier.
    {file_name:file_size}"""
    assert FileManager().get_files_names_sizes(three_files_in_dir_root) == {
        'file_1.txt': 5,
        'file_2.py': 12,
        'file_3.png': 9,
    }


def test_get_files_names_sizes_no_valid_path():
    """Vérifie que 'get_files_names_sizes' retourne un dictionnaire dont les
    clés sont les noms des fichiers et les valeurs sont les tailles du fichier.
    {file_name:file_size}"""
    assert str(FileManager().get_files_names_sizes(Path('no valid path'))) == (
        "[WinError 3] Le chemin d’accès spécifié est introuvable:"
        " 'no valid path'"
    )


def test_diff_between_two_file_dicts():
    """Vérifie que 'diff_between_two_file_dicts' retourne les dossiers de
    dict_1 manquants à dict_2 et les dossiers de dict_2 manquants à dict_1"""
    dict_1 = {'file_1.txt': 12, 'file_2.txt': 58, 'file_3.py': 25}
    dict_2 = {'file_1.txt': 12, 'file_2.txt': 78, 'file_4.png': 525}

    expected_missing_in_dict_2 = [('file_3.py', 25), ('file_2.txt', 58)]
    expected_missing_in_dict_1 = [('file_2.txt', 78), ('file_4.png', 525)]
    (
        missing_in_dict_2,
        missing_in_dict_1,
    ) = FileManager().diff_between_two_file_dicts(dict_1, dict_2)

    assert sorted(missing_in_dict_2) == sorted(expected_missing_in_dict_2)
    assert sorted(missing_in_dict_1) == sorted(expected_missing_in_dict_1)


def test_diff_between_two_file_dicts_dict_1_empty():
    """Vérifie que 'diff_between_two_file_dicts' retourne aucun dossier de
    dict_1 manquants à dict_2 et les dossiers de dict_2 sont tous manquants
    à dict_1"""
    dict_1 = {}
    dict_2 = {'file_1.txt': 12, 'file_2.txt': 78, 'file_4.png': 525}

    expected_missing_in_dict_2 = []
    expected_missing_in_dict_1 = [
        ('file_1.txt', 12),
        ('file_2.txt', 78),
        ('file_4.png', 525),
    ]
    (
        missing_in_dict_2,
        missing_in_dict_1,
    ) = FileManager().diff_between_two_file_dicts(dict_1, dict_2)

    assert sorted(missing_in_dict_2) == sorted(expected_missing_in_dict_2)
    assert sorted(missing_in_dict_1) == sorted(expected_missing_in_dict_1)


def test_diff_between_two_file_dicts_dict_2_empty():
    """Vérifie que 'diff_between_two_file_dicts' retourne aucun dossier de
    dict_2 manquants à dict_1 et les dossiers de dict_1 sont tous manquants
    à dict_2"""
    dict_1 = {'file_1.txt': 12, 'file_2.txt': 58, 'file_3.py': 25}
    dict_2 = {}

    expected_missing_in_dict_2 = [
        ('file_1.txt', 12),
        ('file_2.txt', 58),
        ('file_3.py', 25),
    ]
    expected_missing_in_dict_1 = []
    (
        missing_in_dict_2,
        missing_in_dict_1,
    ) = FileManager().diff_between_two_file_dicts(dict_1, dict_2)

    assert sorted(missing_in_dict_2) == sorted(expected_missing_in_dict_2)
    assert sorted(missing_in_dict_1) == sorted(expected_missing_in_dict_1)


def test_diff_between_two_file_dicts_dict_1_dict_2_empty():
    """Vérifie que 'diff_between_two_file_dicts' retourne 2 listes vides
    lorsque dict_1 et dict_2 sont vides"""
    dict_1 = {}
    dict_2 = {}

    expected_missing_in_dict_2 = []
    expected_missing_in_dict_1 = []
    (
        missing_in_dict_2,
        missing_in_dict_1,
    ) = FileManager().diff_between_two_file_dicts(dict_1, dict_2)

    assert sorted(missing_in_dict_2) == sorted(expected_missing_in_dict_2)
    assert sorted(missing_in_dict_1) == sorted(expected_missing_in_dict_1)


def test_copy_or_update_files_call_shutil(monkeypatch):
    """Verifie que la fonction 'shutil.copy2' soit appelé le bon nombre de fois
    avec les bons arguments"""
    files_to_copy = [('file_1.txt', 12), ('file_2.png', 587)]
    path_target = Path(r'E:\target\target_dir')
    path_source = Path(r'D:\source\source_dir')

    mock_shutil = Mock()
    monkeypatch.setattr(
        "backup_manager_pyside.models.file_manager.shutil", mock_shutil
    )
    FileManager().copy_or_update_files(files_to_copy, path_target, path_source)

    expected_calls = [
        call(
            Path(r'D:\source\source_dir\file_1.txt'),
            Path(r'E:\target\target_dir\file_1.txt'),
        ),
        call(
            Path(r'D:\source\source_dir\file_2.png'),
            Path(r'E:\target\target_dir\file_2.png'),
        ),
    ]
    for called, expected_call in zip(
        mock_shutil.copy2.mock_calls, expected_calls
    ):
        assert called == expected_call


def test_copy_or_update_files_OSError(monkeypatch):
    """Verifie que si 'shutil.copy2' lève une exception OSError,
    celle-ci est gérée."""
    files_to_copy = [('file_1.txt', 12)]
    path_target = Path(r'E:\target\target_dir')
    path_source = Path(r'D:\source\source_dir')

    mock_shutil = Mock()
    monkeypatch.setattr(
        "backup_manager_pyside.models.file_manager.shutil", mock_shutil
    )
    mock_shutil.copy2.side_effect = OSError('error message')

    assert (
        str(
            FileManager().copy_or_update_files(
                files_to_copy, path_target, path_source
            )
        )
        == "error message"
    )


def test_delete_files(three_files_in_dir_root):
    """Vérifie que 'delete_files' supprime la liste de fichiers
    'file_to_delete'"""
    files_to_delete = [('file_1.txt', 5), ('file_2.py', 12)]
    root = three_files_in_dir_root
    FileManager().delete_files(files=files_to_delete, path_target=root)
    get_files = [f.name for f in root.iterdir() if f.is_file()]
    assert ['file_3.png'] == sorted(get_files)


def test_delete_files_OSError(three_files_in_dir_root, monkeypatch):
    """Verifie que si, lors de la suppression d'un fichier, une exception
    OSError est le levée, celle-ci est gérée."""
    files_to_delete = [('file_1.txt', 5)]
    root = three_files_in_dir_root
    mock_unlink = Mock()
    monkeypatch.setattr(
        "backup_manager_pyside.models.directory_manager.Path.unlink",
        mock_unlink,
    )
    mock_unlink.side_effect = OSError('error message')
    assert (
        str(
            FileManager().delete_files(files=files_to_delete, path_target=root)
        )
        == "error message"
    )
