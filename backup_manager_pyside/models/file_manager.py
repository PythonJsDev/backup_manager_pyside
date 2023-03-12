import shutil
from pathlib import Path


class FileManager:
    """gestion des fichiers"""

    def get_files_names_sizes(self, path: Path) -> dict[str, int] | OSError:
        """Retourne un dictionnaire dont les clés sont les noms des fichiers
        et les valeurs sont les tailles du fichier.
        {file_name:file_size}"""
        try:
            return {
                f.name: f.stat().st_size for f in path.iterdir() if f.is_file()
            }
        except OSError as err:
            return err

    def diff_between_two_file_dicts(
        self,
        dict_1: dict[str, int],
        dict_2: dict[str, int],
    ) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
        """Retourne la liste des noms de tuple (nom de fichiers,
        taille du fichier) présents dans 'dict_1' mais pas dans 'dict_2'
        et inversement.
        """
        return (
            [f for f in dict_1.items() if f not in dict_2.items()],
            [f for f in dict_2.items() if f not in dict_1.items()],
        )

    def copy_or_update_files(
        self,
        files: list[tuple[str, int]],
        path_target: Path,
        path_src: Path,
    ):
        """Copie sur la cible, dans le dossier pointé par 'path_target', les
        fichiers présents dans la liste 'files'"""
        for file in files:
            try:
                src = path_src / file[0]
                target = path_target / file[0]
                # print('file_to_copy', src, target)
                shutil.copy2(src, target)
            except OSError as err:
                return err

    def delete_files(
        self,
        files: list[tuple[str, int]],
        path_target: Path,
    ):
        """Efface sur la cible, dans le dossier pointé par 'path_target', les
        fichiers présents dans la liste 'files'"""
        for file in files:
            try:
                file_to_delete = Path(path_target / file[0])
                # print('file_to_delete', file_to_delete)
                file_to_delete.unlink()
            except OSError as err:
                return err
