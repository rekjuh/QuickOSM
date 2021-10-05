"""Set up a completer that ignore diacritics and accents"""

import unicodedata

from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QCompleter


def strip_accents(s: str) -> str:
    """Decode diacritic text"""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


class DiacriticFreeCompleter(QCompleter):
    """Set up a custom completer that ignore diacritic"""

    def splitPath(self, path: str) -> list:
        """Manage diacritic elements"""
        return [strip_accents(path).lower()]

    def pathFromIndex(self, index):
        """Return the path at the given index"""
        return index.data()


class DiactricFreeStringListModel(QStringListModel):
    """Set up a custom model for the custom completer"""

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super(DiactricFreeStringListModel, self).__init__(*args, **kwargs)
        self.setDiactricFreeRole(Qt.UserRole + 10)

    def data(self, index, role: int) -> str:
        """Handle the diacritic elements"""
        if role == self.diactricFreeRole():
            value = super(DiactricFreeStringListModel, self).data(index, Qt.DisplayRole)
            return strip_accents(value).lower()
        return super(DiactricFreeStringListModel, self).data(index, role)

    def setDiactricFreeRole(self, role: int):
        """Set the diacritic free role"""
        self.mDiactricFreeRole = role

    def diactricFreeRole(self) -> int:
        """Get the diacritic free role"""
        return self.mDiactricFreeRole