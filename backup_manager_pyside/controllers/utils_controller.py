from pathlib import Path

from ..models import directory_manager
from ..views import utils_views
from ..views.info_dialog import InfoDialog

# from ..views.utils_views import warning_msg, info_msg
# from ..views.utils_views import info_msg


def display_message_if_error(obj, main_window) -> bool:
    """Affiche dans une message box une erreur de type OSError"""
    if isinstance(obj, OSError):
        utils_views.error_msg(
            main_window, f"{obj.strerror}:\n'{obj.filename}'"
        )
        return True
    return False


def display_info_if_empty(path, main_window):
    """Affiche en message box si le dossier pointé par path est vide"""
    utils_views.warning_msg(main_window, f"Le dossier '{str(path)}' est vide.")


def ask_to_confirm(title, message, data_list, parent):
    """Affiche une fenêtre modale pour afficher une liste de dossier
    ou de fichiers et demande la confirmation à l'action proposée"""
    dlg = InfoDialog(title, message, data_list, parent)
    if dlg.exec():
        return True
    return False


def to_cancel(self, main_window):
    """Annule l'action en cours"""
    self.app_canceled = True
    cancel_controller(self, main_window)
    utils_views.info_msg(
        main_window, "Annulation", "La mise à jour est annulée."
    )


def cancel_controller(self, main_window):
    """Efface toutes les listes et réinitialise l'ui"""
    self.missing_folders = []
    self.excess_folders = []
    self.missing_files = []
    self.excess_files = []
    self.sub_folders_src = []
    self.sub_folders_target = []
    utils_views.cancel(main_window)


def display_list_dirs_to_create(self) -> bool:
    """Affiche en popup la liste des dossiers à créer et demande l'accord de
    l'utilisateur pour cette action"""

    message = plural_or_singular_msg(
        self, self.missing_folders, "dossier", create=True
    )
    title = "Mise à jour des dossiers"
    return ask_to_confirm(
        title, message, sorted(self.missing_folders), self.main_window
    )


def display_list_dirs_to_delete(self) -> bool:
    """Affiche en popup la liste des dossiers à supprimer et demande l'accord
    de l'utilisateur pour cette action"""

    message = plural_or_singular_msg(
        self, self.excess_folders, "dossier", create=False
    )
    title = "Mise à jour des dossiers"
    return ask_to_confirm(
        title,
        message,
        sorted(self.excess_folders, reverse=True),
        self.main_window,
    )


def plural_or_singular_msg(
    self,
    item_list: list[Path],
    item: str,
    create: bool = True,
) -> str:
    place = f" dans le dossier: \n'{str(self.target)}'"
    if len(item_list) > 1:
        if create:
            return (
                f'Les {item}s suivants vont être créés sur la cible'
                f"{place}\n"
                f'{len(item_list)} {item}s'
            )
        else:
            return (
                f'Les {item}s suivants vont être supprimés sur la cible'
                f"{place}\n"
                f'{len(item_list)} {item}s'
            )
    if create:
        if item_list:
            return (
                f"Le {item} '{str(item_list[0])}' va être créé sur la cible"
                f"{place}"
            )
    else:
        if item_list:
            return (
                f"Le {item} '{str(item_list[0])}' va être supprimé sur"
                " la cible"
                f"{place}\n"
            )


def display_list_files_to_delete(self, folder) -> bool:
    """Affiche en popup la liste des fichiers à supprimer et demande l'accord
    de l'utilisateur pour cette action"""
    message = (
        'Les fichiers suivants vont être supprimés sur la cible'
        f' dans le dossier: \n{self.target/folder}:'
    )
    title = "Mise à jour des fichiers"
    return ask_to_confirm(
        title, message, sorted(self.excess_files), self.main_window
    )


def display_list_files_to_create(self, folder) -> bool:
    """Affiche en popup la liste des fichiers à créer et demande l'accord de
    l'utilisateur pour cette action"""
    message = (
        'Les fichiers suivants vont être copiés ou mis à jour sur la cible'
        f' dans le dossier: \n{self.target/folder}:'
    )
    title = "Mise à jour des fichiers"
    return ask_to_confirm(
        title, message, sorted(self.missing_files), self.main_window
    )


def filtering_list_items(
    folders: list[Path], to_ignore: list[Path]
) -> list[Path]:
    """Retourne une liste ne contenant plus les items spécifiés dans
    to_ignore"""
    to_remove = [
        x for x in folders for i in to_ignore if str(x).find(str(i)) != -1
    ]

    return list(set(folders).difference(to_remove))


def valid_target_path(self, main_window):
    if self.src.name != self.target.name:
        utils_views.warning_msg(
            main_window,
            ("Les dossiers 'source' et 'cible' doivent avoir le même nom."),
        )
        already_exist = existing_folder(self.target, self.src, main_window)
        if isinstance(already_exist, OSError):
            utils_views.info_msg(
                main_window,
                "Dossier invalide.",
                "Veuiller modifier le dossier cible.",
            )
            return False
        else:
            if already_exist:
                utils_views.info_msg(
                    main_window,
                    "Dossier existant.",
                    f"{already_exist}\nVeuillez modifier le dossier cible.",
                )
                return False
            else:
                if utils_views.authorize_an_action(
                    main_window,
                    'Action',
                    f"Voulez-vous créer le dossier '{self.src.name}'?",
                ):
                    self.target = self.target / Path(self.src.name)
                    self.target.mkdir(exist_ok=True)
                    utils_views.update_text_edit_path_dirs(
                        main_window, self.src, self.target
                    )
                    return False
                else:
                    utils_views.info_msg(
                        main_window,
                        "Dossier inexistant",
                        (
                            f"Le dossier '{self.src.name}' n'existe pas sur la"
                            " cible\nVeuillez modifier le dossier cible."
                        ),
                    )
                    return False
    return True


def existing_folder(
    target_path: Path, src_path: Path, main_window
) -> str | OSError | bool:
    """vérifie si le dossier passé dans target-path existe"""
    sub_folders_target = (
        directory_manager.DirectoryManager().get_subdirectories(target_path)
    )
    if display_message_if_error(sub_folders_target, main_window):
        return sub_folders_target
    for folder in sub_folders_target:
        if str(folder).find(src_path.name) != -1:
            return f"Le dossier '{str(target_path/folder)}' existe"
    return False
