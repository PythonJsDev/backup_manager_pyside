from ..views import utils_views
from ..views.info_dialog import InfoDialog
from ..views.utils_views import info_msg


def display_message_if_error(obj, main_window) -> bool:
    """Affiche dans une message box une erreur de type OSError"""
    if isinstance(obj, OSError):
        utils_views.error_msg(
            main_window, f"{obj.strerror}:\n'{obj.filename}'")
        return True
    return False


def display_info_if_empty(path, main_window):
    """Affiche en message box si le dossier pointé par path est vide"""
    utils_views.warning_msg(main_window, f"Le dossier '{str(path)}' est vide")


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
    info_msg(main_window, "Annulation", "La mise à jour est annulée")


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
    message = (
        'Les dossiers suivants vont être créés sur la cible'
        f' dans le dossier: \n{str(self.target)}:'
    )
    title = "Mise à jour des dossiers"
    return ask_to_confirm(
        title, message, sorted(self.missing_folders), self.main_window
    )


def display_list_dirs_to_delete(self) -> bool:
    """Affiche en popup la liste des dossiers à supprimer et demande l'accord
    de l'utilisateur pour cette action"""
    message = (
        'Les dossiers suivants vont être supprimés sur la cible'
        f' dans le dossier: \n{str(self.target)}:'
    )
    title = "Mise à jour des dossiers"
    return ask_to_confirm(
        title,
        message,
        sorted(self.excess_folders, reverse=True),
        self.main_window,
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
