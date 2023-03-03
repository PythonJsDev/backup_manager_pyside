from pathlib import Path
from .models.directory_manager import DirectoryManager
from .models.file_manager import FileManager

from .controllers.directory_controller import DirectoryController


def main():
    source = Path(r'D:\users\test backup manager')
    target = Path(r'D:\users\test backup manager - target')
    directory = DirectoryManager()
    file = FileManager()
    sub_folders_src = directory.get_subdirectories(source)
    print('SOURCE', len(sub_folders_src))
    for f in sub_folders_src:
        print(f)
    sub_folders_target = directory.get_subdirectories(target)
    print()
    print('TARGET', len(sub_folders_target))
    for f in sub_folders_target:
        print(f)
    # print(sub_folders_src, sub_folders_target)
    missing_folders, excess_folders = directory.diff_between_two_folder_lists(
        sub_folders_src, sub_folders_target
    )
    print()
    print('MISSING')
    print(missing_folders)
    print()
    print('EXCESS')
    print(excess_folders)
    directory.create_folders(target, missing_folders)
    directory.delete_folders(target, excess_folders)
    files_src = file.get_files_names_sizes(source)
    print()
    print('files src', len(files_src))
    files_target = file.get_files_names_sizes(target)
    print()
    print('files target', len(files_target))
    print()
    files_to_copy, file_to_delete = file.diff_between_two_file_dicts(
        files_src, files_target
    )
    print('FILE To COPY or UPDATE')
    print(files_to_copy)

    file.copy_or_update_files(
        files=files_to_copy, path_target=target, path_source=source
    )


def mainb():
    root = Path(r'D:\users\test backup manager')
    DirectoryController().get_folders_tree_structure(root)


if __name__ == "__main__":
    main()
