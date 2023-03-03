import shutil
from pathlib import Path

from ..views.message import Message


class DirectoryManager:
    """Gestion des dossiers"""

    def get_last_folder(self, path: Path) -> str:
        """Retourne le nom du dernier dossier du chemin."""
        if path.is_dir():
            return path.name
        return path.parent.name

    def get_subdirectories(self, path: Path) -> list[Path]:
        """Retourne la liste des chemins de tous les
        sous-dossiers pointé par path."""
        return [x.relative_to(path) for x in path.rglob("*") if x.is_dir()]

    def create_folders(self, path: Path, folders: list[str]):
        """Création des dossiers à l'emplacement précisé par le path et
        dont les noms sont listés dans folders."""
        for folder in folders:
            try:
                Path(path, folder).mkdir(exist_ok=True)
            except OSError as err:
                Message().error_msg(f"Une erreur s'est produite !! : {err}")

    def delete_folders(self, path: Path, folders: list[str]):
        """Suppression des dossiers et de tout ce qu'ils contiennent à
        l'emplacement précisé par le path et dont les noms sont listés dans
        folders."""
        for folder in folders:
            try:
                to_delete = Path(path, folder)
                # print('to_delete', to_delete)
                shutil.rmtree(to_delete)
            except OSError as err:
                Message().error_msg(f"Une erreur s'est produite !! : {err}")

    def diff_between_two_folder_lists(
        self, list_1: list[Path], list_2: list[Path]
    ) -> tuple[list[str], list[str]]:
        """Retourne la liste des noms de dossiers présents dans
        la list_1 mais pas dans la list_2 et inversement.
        """
        folders_list_1 = [i1 for i1 in list_1]
        folders_list_2 = [i2 for i2 in list_2]
        return (
            list(set(folders_list_1).difference(folders_list_2)),
            list(set(folders_list_2).difference(folders_list_1)),
        )


if __name__ == "__main__":
    test = DirectoryManager()
    print(f"Chemin du dossier courant {test.get_current_directory_path()}")
    print(f"dossier courant {test.get_current_directory_name()}")
    folder = test.get_last_folder(
        Path(r'D:\users\maury\DEV\cours_python\tests divers')
    )
    print(f"last folder : {folder}", type(folder))
    folder_file = test.get_last_folder(
        Path(r'D:\users\maury\DEV\cours_python\tests divers\settings.py')
    )
    print(f"last folder : {folder_file}")
    print(test.get_subdirectories(Path(r'D:\users\test backup manager')))
