from pathlib import Path
FOLDERS_TO_IGNORE = [
    Path('.venv'),
    Path('env'),
    Path('__pycache__'),
    Path('.pytest_cache'),
    Path('.mypy_cache'),
    Path('.vscode'),
    Path('.git'),
]
