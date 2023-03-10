from pathlib import Path

from ..models.directory_manager import DirectoryManager
from ..models.file_manager import FileManager
from ..views.info_dialog import InfoDialog


class AppController:
    # def __init__(self) -> None:
    #     self.missing_folders = []
    #     self.excess_folders = []

    def app_controller(self, dirs_path):
        self.directory_controller(dirs_path)
        self.file_controller()

    def directory_controller(self, dirs_path):
        self.source = Path(dirs_path.get('src'))
        self.target = Path(dirs_path.get('target'))
        directory = DirectoryManager()

        self.sub_folders_src = directory.get_subdirectories(self.source)
        print('SOURCE', len(self.sub_folders_src))
        for f in self.sub_folders_src:
            print(f)
        sub_folders_target = directory.get_subdirectories(self.target)
        print()
        print('TARGET', len(sub_folders_target))
        for f in sub_folders_target:
            print(f)
        # print(sub_folders_src, sub_folders_target)
        (
            self.missing_folders,
            self.excess_folders,
        ) = directory.diff_between_two_folder_lists(
            self.sub_folders_src, sub_folders_target
        )
        print()
        print('MISSING')
        print(self.missing_folders)
        print()
        print('EXCESS')
        print(self.excess_folders)
        message = (
            'Les dossiers suivants vont être créés sur la cible'
            f' dans le dossier: \n{self.target}:'
        )
        dlg = InfoDialog(
            'Mise à jour des dossiers', message, self.missing_folders
        )
        if dlg.exec():
            print('------ Success ! -----------')
            directory.create_folders(self.target, self.missing_folders)
        else:
            print('------ Cancel ! ------------')

        message = (
            'Les dossiers suivants vont être supprimés sur la cible'
            f' dans le dossier: \n{self.target}:'
        )
        dlg = InfoDialog(
            'Mise à jour des dossiers', message, self.excess_folders
        )
        if dlg.exec():
            print('------ Success ! -----------')
            directory.delete_folders(self.target, self.excess_folders)
        else:
            print('------ Cancel ! ------------')

    def file_controller(self):
        print('----------- file controller ------------------')
        # print('missing', self.missing_folders)
        file = FileManager()
        for folder in self.sub_folders_src:
            print(self.source/folder)
            src_files = file.get_files_names_sizes(self.source/folder)
            print('*', src_files)
            
