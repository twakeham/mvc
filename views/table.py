import typing

from PyQt5.QtCore import QModelIndex, QObject
from PyQt5.QtWidgets import QTableView

from db import proxy
from db import model
from utils import events


class TableColumn(QObject):

    def __init__(self, field: model.DatabaseField, table: QTableView) -> None:
        super().__init__()
        self.field = field
        self.table = table

    def show(self):
        self.table.setColumnHidden(self.field.index, False)

    def hide(self):
        self.table.setColumnHidden(self.field.index, True)


class TableView(QTableView, events.EventConnector):

    def __init__(self, model: model.DatabaseModel) -> None:
        super().__init__()

        # setup models
        self.data_model = model
        self.proxy_model = proxy.CustomSortFilterProxyModel()
        self.proxy_model.setSourceModel(model)

        self.setModel(self.proxy_model)

        self.columns = []  # type: typing.List[TableColumn]
        for field in self.data_model.fields:
            column = TableColumn(field, self)
            self.columns.append(column)
            setattr(self, field.name, column)

    def get_selected_indexes(self) -> typing.List[QModelIndex]:
        indexes = self.selectedIndexes()
        return [self.proxy_model.mapToSource(index) for index in indexes]

    def get_selected_index(self) -> QModelIndex:
        indexes = self.selectedIndexes()
        return self.proxy_model.mapToSource(indexes[0]) if indexes else None

    def get_selected_records(self):
        indexes = self.get_selected_indexes()
        return [self.data_model.record(index.row()) for index in indexes]