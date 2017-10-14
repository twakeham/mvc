import typing

from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex
from PyQt5.QtSql import QSqlRecord


class CustomSortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.filter_functions = {}

    def add_filter_function(self, name: str, filter_function: typing.Callable[[QSqlRecord, str], bool]) -> None:
        self.filter_functions[name] = filter_function
        self.invalidateFilter()

    def clear_filter_functions(self) -> None:
        self.filter_functions = {}
        self.invalidateFilter()

    def remove_filter_function(self, name: str) -> bool:
        if name in self.filter_functions:
            del self.filter_functions[name]
            return True
        return False

    def update(self):
        self.invalidateFilter()

    # QT override
    def filterAcceptsRow(self, row: int, parent: QModelIndex) -> bool:
        model = self.sourceModel()
        tests = [func(model.record(row), self.filterString)
                 for func in self.filter_functions.values()]
        return (False not in tests) and super().filterAcceptsRow(row, parent)