from PySide6 import QtCore, QtWidgets

from backup_manager_pyside.controllers.app_controller import AppController
from .utils_views import cancel
from .constants import BTN_HEIGHT, BTN_WIDTH, MAIN_WIN_HEIGHT, MAIN_WIN_WIDTH

from .utils_views import separator_hline, get_dirname


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.dirs_path = {}
        self.setWindowTitle("Backup Manager")
        self.resize(MAIN_WIN_WIDTH, MAIN_WIN_HEIGHT)
        self.setup_ui()
        widget = QtWidgets.QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def setup_ui(self):
        self.create_layout()
        self.create_widgets()
        self.add_widgets_to_QGridLayout()

    def create_layout(self):
        self.main_layout = QtWidgets.QGridLayout()

    def create_widgets(self):
        # labels
        self.lbl_title = QtWidgets.QLabel("Backup Manager")
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setFixedHeight(40)

        self.hline_top = separator_hline(self, name='hline_top', thick=3)
        # text edit
        self.te_dirs = QtWidgets.QTextEdit()
        self.te_dirs.setReadOnly(True)
        # buttons
        self.btn_src = QtWidgets.QPushButton('Dossier source')
        self.btn_src.setEnabled(True)
        self.btn_src.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.btn_src.clicked.connect(lambda: get_dirname(self, 'src'))

        self.btn_target = QtWidgets.QPushButton('Dossier cible')
        self.btn_target.setEnabled(False)
        self.btn_target.clicked.connect(lambda: get_dirname(self, 'target'))
        self.btn_target.setFixedSize(BTN_WIDTH, BTN_HEIGHT)

        self.btn_quit = QtWidgets.QPushButton("Quitter")
        self.btn_quit.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.btn_quit.clicked.connect(self.close)

        self.btn_valid = QtWidgets.QPushButton("Valider")
        self.btn_valid.setEnabled(False)
        self.btn_valid.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.btn_valid.clicked.connect(
            lambda: AppController().app_controller(self.dirs_path, self)
        )
        self.btn_cancel = QtWidgets.QPushButton("Annuler")
        self.btn_cancel.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.btn_cancel.clicked.connect(lambda: cancel(self))

    def add_widgets_to_QGridLayout(self):
        self.main_layout.addWidget(self.lbl_title, 0, 0, 1, 4)
        self.main_layout.addWidget(self.hline_top, 1, 0, 1, 4)

        self.main_layout.addWidget(self.btn_src, 2, 0, 1, 1)
        self.main_layout.addWidget(self.btn_target, 3, 0, 1, 1)

        self.main_layout.addWidget(self.te_dirs, 5, 0, 1, 4)

        self.main_layout.addWidget(self.btn_quit, 7, 3, 1, 1)
        self.main_layout.addWidget(self.btn_cancel, 7, 1, 1, 1)
        self.main_layout.addWidget(self.btn_valid, 7, 0, 1, 1)

        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

    def closeEvent(self, event):
        self.replyClosing = QtWidgets.QMessageBox.question(
            self,
            'Message',
            "Êtes-vous sûr de vouloir quitter ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )

        if self.replyClosing == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
