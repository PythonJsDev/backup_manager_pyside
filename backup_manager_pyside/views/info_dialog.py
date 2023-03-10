from PySide6 import QtWidgets


class InfoDialog(QtWidgets.QDialog):
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
