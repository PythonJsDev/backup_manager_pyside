def load_styles(app):
    with open(r"backup_manager_pyside\statics\styles\style.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
