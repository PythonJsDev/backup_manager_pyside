from pathlib import Path
from .constants_controller import FOLDERS_TO_IGNORE
from ..models.directory_manager import DirectoryManager
from ..models.file_manager import FileManager
from ..views.utils_views import info_msg
from .utils_controller import (
    display_message_if_error,
    display_info_if_empty,
    to_cancel,
    cancel_controller,
    display_list_dirs_to_create,
    display_list_dirs_to_delete,
    display_list_files_to_create,
    display_list_files_to_delete,
    filtering_list_items,
    valid_target_path,
)


class AppController:
    def __init__(self) -> None:
        self.directory = DirectoryManager()
        self.file = FileManager()
        self.app_canceled = False
        self.missing_folders: list[Path] = []
        self.excess_folders: list[Path] = []
        self.missing_files: list[tuple[str, int]] = []
        self.excess_files: list[tuple[str, int]] = []

    def app_controller(self, dirs_path: dict[str, str], main_window):
        self.main_window = main_window
        self.get_difference_between_dirs_src_and_target(dirs_path)

    def get_difference_between_dirs_src_and_target(
        self, dirs_path: dict[str, str]
    ):
        """Détermine les dossiers manquants et les dossiers en exces sur
        la cible"""
        self.src = Path(dirs_path.get('src', ''))
        self.target = Path(dirs_path.get('target', ''))
        if valid_target_path(self, self.main_window):
            self.sub_folders_src = self.directory.get_subdirectories(self.src)
            display_message_if_error(self.sub_folders_src, self.main_window)
            if not self.sub_folders_src:
                display_info_if_empty(self.src, self.main_window)
            else:
                self.sub_folders_target = self.directory.get_subdirectories(
                    self.target
                )
                display_message_if_error(
                    self.sub_folders_target, self.main_window
                )
                (
                    self.missing_folders,
                    self.excess_folders,
                ) = self.directory.diff_between_two_folder_lists(
                    self.sub_folders_src, self.sub_folders_target
                )
                self.missing_folders = filtering_list_items(
                    self.missing_folders, FOLDERS_TO_IGNORE
                )
                self.update_directories_controller()

    def update_directories_controller(self):
        """Controle de la création des dossiers manquants et de la suppression
        des dossiers en exces sur la cible"""
        if self.missing_folders:
            if display_list_dirs_to_create(self):
                created_dir = self.directory.create_folders(
                    self.target, sorted(self.missing_folders)
                )
                display_message_if_error(created_dir, self.main_window)
            else:
                to_cancel(self, self.main_window)

        if not self.app_canceled and self.excess_folders:
            if display_list_dirs_to_delete(self):
                deleted_dir = self.directory.delete_folders(
                    self.target, sorted(self.excess_folders, reverse=True)
                )
                display_message_if_error(deleted_dir, self.main_window)
            else:
                to_cancel(self, self.main_window)
        self.update_files_controller()

    def update_files_controller(self):
        """Controle de la création des fichiers manquants et de la suppression
        des fichiers en exces sur la cible"""
        if not self.app_canceled:
            self.sub_folders_src = filtering_list_items(
                self.sub_folders_src, FOLDERS_TO_IGNORE
            )
            self.sub_folders_src.insert(0, Path(''))

            for folder in self.sub_folders_src:
                if not self.get_difference_between_files_src_and_target(
                    folder
                ):
                    continue

                if self.excess_files:
                    if display_list_files_to_delete(self, folder):
                        deleted_file = self.file.delete_files(
                            sorted(self.excess_files), self.target / folder
                        )
                        display_message_if_error(
                            deleted_file, self.main_window
                        )
                    else:
                        to_cancel(self, self.main_window)
                        break
                if self.missing_files:
                    if display_list_files_to_create(self, folder):
                        created_file = self.file.copy_or_update_files(
                            sorted(self.missing_files),
                            self.target / folder,
                            self.src / folder,
                        )
                        display_message_if_error(
                            created_file, self.main_window
                        )
                    else:
                        to_cancel(self, self.main_window)
                        break

            if not self.app_canceled:
                info_msg(
                    self.main_window,
                    "C'est fait !",
                    "La mise à jour est terminée",
                )
                cancel_controller(self, self.main_window)

    def get_difference_between_files_src_and_target(
        self, folder: Path
    ) -> bool:
        self.missing_files = []
        self.excess_files = []
        src_files = self.file.get_files_names_sizes(self.src / folder)

        if display_message_if_error(src_files, self.main_window):
            return False
        target_files = self.file.get_files_names_sizes(self.target / folder)
        if display_message_if_error(target_files, self.main_window):
            return False
        if not isinstance(src_files, OSError) and not isinstance(
            target_files, OSError
        ):
            (
                self.missing_files,
                self.excess_files,
            ) = self.file.diff_between_two_file_dicts(src_files, target_files)

        return True
