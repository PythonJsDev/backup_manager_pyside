from pathlib import Path

from PySide6 import QtWidgets


def separator_hline(self, name: str = 'Hline', thick: int = 1):
    self.separator_line = QtWidgets.QFrame()
    self.separator_line.setFrameShape(QtWidgets.QFrame.HLine)
    self.separator_line.setLineWidth(thick)
    self.separator_line.setObjectName(name)
    return self.separator_line


def get_dirname(self, cat: str):
    directory = dialog_directories()
    if directory:
        if cat == 'src':
            self.dirs_path['src'] = Path(directory)
            self.btn_target.setEnabled(True)
            msg = f"Dossier source:\n{self.dirs_path.get('src')}\n"
        else:
            # self.btn_src.setEnabled(False)
            self.dirs_path['target'] = Path(directory)
            msg = (
                f"Dossier source:\n{self.dirs_path.get('src')}\n"
                f"Dossier cible:\n{self.dirs_path.get('target')}\n"
            )
        self.te_dirs.setText(msg)
        valid_dirs_path(self, self.dirs_path)


def dialog_directories():
    """Affiche la boite de dialogue pour choisir un dossier"""
    return QtWidgets.QFileDialog.getExistingDirectory()


def valid_dirs_path(self, dirs_path: dict[str, Path]):
    if dirs_path.get('src') and dirs_path.get('target'):
        if dirs_path.get('src') == dirs_path.get('target'):
            warning(
                self,
                ("Les dossiers source et cible doivent " "être différents !"),
            )
            self.btn_valid.setEnabled(False)
        else:
            self.btn_valid.setEnabled(True)


def warning(self, message: str):
    QtWidgets.QMessageBox.warning(
        self,
        'Attention !',
        message,
    )


# def cancel(self):
#     self.te_dirs.clear()
#     self.btn_valid.setEnabled(False)
#     self.btn_target.setEnabled(False)
#     self.dirs_path = {}
