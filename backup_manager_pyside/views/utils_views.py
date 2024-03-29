from pathlib import Path

from PySide6 import QtWidgets


def separator_hline(self, name: str = 'Hline', thick: int = 1):
    """Création d'une ligne horizontale d'épaisseur 'thick'"""
    self.separator_line = QtWidgets.QFrame()
    self.separator_line.setFrameShape(QtWidgets.QFrame.HLine)
    self.separator_line.setLineWidth(thick)
    self.separator_line.setObjectName(name)
    return self.separator_line


def get_dirname(self, cat: str):
    """Range dans un dictionnaire les chemins des dossiers source et cible.
    dirs_path = {'src': Path(path_src), 'target': Path(path_target)}
    et l'affiche dans le textEdit"""
    directory = dialog_directories()
    if directory:
        if cat == 'src':
            self.dirs_path['src'] = Path(directory)
            self.btn_target.setEnabled(True)
            msg = f"Dossier source:\n{self.dirs_path.get('src')}\n"
        else:
            self.dirs_path['target'] = Path(directory)
            msg = (
                f"Dossier source:\n{self.dirs_path.get('src')}\n"
                f"Dossier cible:\n{self.dirs_path.get('target')}\n"
            )
        self.te_dirs.setText(msg)
        valid_dirs_path(self, self.dirs_path)


def update_text_edit_path_dirs(self, src_path, target_path):
    """Mise à jour du textEdit affichant les chemins des dossiers 'source' et
    'cible'"""
    msg = (
        f"Dossier source:\n{str(src_path)}\n"
        f"Dossier cible:\n{str(target_path)}\n"
    )
    self.dirs_path['target'] = target_path
    self.te_dirs.setText(msg)


def dialog_directories():
    """Affiche la boite de dialogue pour choisir un dossier"""
    return QtWidgets.QFileDialog.getExistingDirectory()


def valid_dirs_path(self, dirs_path: dict[str, Path]):
    """Active le bouton 'Valider' si les chemins du dossier source et du
    chemin 'cible' sont différents"""
    if dirs_path.get('src') and dirs_path.get('target'):
        src_path = dirs_path.get('src')
        target_path = dirs_path.get('target')
        if src_path == target_path:
            warning_msg(
                self,
                (
                    "Les chemins des dossiers 'source' et 'cible' doivent être"
                    " différents !"
                ),
            )
            self.btn_valid.setEnabled(False)
        else:
            self.btn_valid.setEnabled(True)


def warning_msg(self, message: str):
    """Fenêtre modale pour afficher un warning"""
    QtWidgets.QMessageBox.warning(
        self,
        'Attention !',
        message,
    )


def error_msg(self, message: str):
    """Fenêtre modale pour afficher une erreur"""
    QtWidgets.QMessageBox.critical(
        self,
        'Erreur critique !',
        message,
        buttons=QtWidgets.QMessageBox.Ok,
    )


def info_msg(self, title: str, message: str):
    """Fenêtre modale pour afficher un message d'info"""
    QtWidgets.QMessageBox.information(
        self,
        title,
        message,
    )


def authorize_an_action(self, title: str, message: str):
    """Fenêtre modale pour autoriser une action"""
    button = QtWidgets.QMessageBox.question(
        self,
        title,
        message,
    )
    if button == QtWidgets.QMessageBox.Yes:
        return True
    if button == QtWidgets.QMessageBox.No:
        return False
    return False


def cancel(self):
    """Remise à zéro du l'interface utilisateur"""
    self.te_dirs.clear()
    self.btn_valid.setEnabled(False)
    self.btn_target.setEnabled(False)
    self.dirs_path = {}


class ItemDialog(QtWidgets.QDialog):
    def __init__(self, title, message, items, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(title)
        self.te_txt = QtWidgets.QTextEdit()
        self.te_txt.setReadOnly(True)
        items_str = [str(i) for i in items]
        self.te_txt.setText('\n'.join(items_str))
        buttons = (
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        self.buttonBox = QtWidgets.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.msg = QtWidgets.QLabel(message)

        self.layout.addWidget(self.msg)
        self.layout.addWidget(self.te_txt)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
