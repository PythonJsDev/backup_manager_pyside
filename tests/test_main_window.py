from pathlib import Path
from unittest import mock

import pytest
from PySide6 import QtWidgets

from backup_manager_pyside.views import utils_views
from backup_manager_pyside.views.main_window import MainWindow


@pytest.fixture
def main_app(qtbot, monkeypatch):
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    #  mock le QMessageBox.question présent dans la methode: closeEvent
    monkeypatch.setattr(
        QtWidgets.QMessageBox,
        "question",
        lambda *args: QtWidgets.QMessageBox.No,
    )
    #  mock le QMessageBox.warning présent dans la methode: warning
    monkeypatch.setattr(
        QtWidgets.QMessageBox,
        "warning",
        lambda *args: QtWidgets.QMessageBox.Ok,
    )

    return main_window


def test_main_window_title(main_app):
    """Vérifie le titre de la fenêtre principale"""
    assert main_app.windowTitle() == "Backup Manager"


def test_src_button(main_app):
    """Vérifie le label et l'activation du bouton 'Dossier source'"""
    assert main_app.btn_src.text() == 'Dossier source'
    assert main_app.btn_src.isEnabled()


def test_target_button(main_app):
    """Vérifie le label et la déactivation du bouton 'Dossier target'"""
    assert main_app.btn_target.text() == 'Dossier cible'
    assert not main_app.btn_target.isEnabled()


def test_valid_button(main_app):
    """Vérifie le label et la déactivation du bouton 'Valider'"""
    assert main_app.btn_valid.text() == 'Valider'
    assert not main_app.btn_valid.isEnabled()


def test_cancel_button(main_app):
    """Vérifie le label et l'activation du bouton 'Annuler'"""
    assert main_app.btn_cancel.text() == 'Annuler'
    assert main_app.btn_cancel.isEnabled()


def test_quit_button(main_app):
    """Vérifie le label et l'activation du bouton 'Quitter'"""
    assert main_app.btn_quit.text() == 'Quitter'
    assert main_app.btn_quit.isEnabled()


def test_valid_dirs_path_same_folder_path(main_app):
    """Vérifie que si les dossiers source et cible sont identiques alors le
    bouton 'Valider' est désactivé"""
    dirs_path = {
        'src': Path(r"D\root_src\dirmame_a"),
        'target': Path(r"D\root_src\dirmame_a"),
    }
    utils_views.valid_dirs_path(main_app, dirs_path)
    assert not main_app.btn_valid.isEnabled()


def test_valid_dirs_path_different_folder_path(main_app):
    """Vérifie que si les dossiers source et cible sont différents alors le
    bouton 'Valider' est activé"""
    dirs_path = {
        'src': Path(r"D\root_src\dirmame_a"),
        'target': Path(r"D\root_target\dirmame_a"),
    }
    utils_views.valid_dirs_path(main_app, dirs_path)
    assert main_app.btn_valid.isEnabled()


def test_valid_dirs_src_path_none(main_app):
    """Vérifie que si les dossiers source est None alors le
    bouton 'Valider' est désactivé"""
    dirs_path = {
        'src': None,
        'target': Path(r"D\root_target\dirmame_a"),
    }
    utils_views.valid_dirs_path(main_app, dirs_path)
    assert not main_app.btn_valid.isEnabled()


def test_valid_dirs_target_path_none(main_app):
    """Vérifie que si les dossiers cible est None alors le
    bouton 'Valider' est désactivé"""
    dirs_path = {
        'src': Path(r"D\root_src\dirmame_a"),
        'target': None,
    }
    utils_views.valid_dirs_path(main_app, dirs_path)
    assert not main_app.btn_valid.isEnabled()


def test_valid_dirs_target_and_src_path_none(main_app):
    """Vérifie que si les dossiers source et cible sont None alors le
    bouton 'Valider' est désactivé"""
    dirs_path = {
        'src': None,
        'target': None,
    }
    utils_views.valid_dirs_path(main_app, dirs_path)
    assert not main_app.btn_valid.isEnabled()


def test_get_dirname_src(main_app, monkeypatch):
    """Vérifie que le chemin du dossier source s'affiche dans le QTextedit"""

    def mock_dialog_directories():
        return r"D:\root_path\src"

    def mock_valid_dirs_path(self, dirs_path):
        return None

    monkeypatch.setattr(
        "backup_manager_pyside.views.utils_views.dialog_directories",
        mock_dialog_directories,
    )
    monkeypatch.setattr(
        "backup_manager_pyside.views.utils_views.valid_dirs_path",
        mock_valid_dirs_path,
    )
    utils_views.get_dirname(main_app, 'src')
    assert (
        main_app.te_dirs.toPlainText().replace('\n', '')
        == r'Dossier source:D:\root_path\src'
    )


def test_get_dirname_src_and_target(main_app, monkeypatch):
    """Vérifie que les chemins des dossiers source et cible s'affichent
    dans le QTextedit"""
    src_path = r"D:\root_path\src"
    target_path = r"D:\root_path\target"
    mock_dialog_directories = mock.Mock()
    mock_dialog_directories.side_effect = [src_path, target_path]
   
    def mock_valid_dirs_path(self, dirs_path):
        return None

    monkeypatch.setattr(
        "backup_manager_pyside.views.utils_views.dialog_directories",
        mock_dialog_directories,
    )
    monkeypatch.setattr(
        "backup_manager_pyside.views.utils_views.valid_dirs_path",
        mock_valid_dirs_path,
    )
    utils_views.get_dirname(main_app, 'src')
    utils_views.get_dirname(main_app, 'target')
    assert (
        main_app.te_dirs.toPlainText().replace('\n', '')
        == r"Dossier source:D:\root_path\srcDossier cible:D:\root_path\target"
    )
