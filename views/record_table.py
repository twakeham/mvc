import typing

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon

from .table import TableView
from .toolbar.record import RecordToolbar


class RecordTableView(QMainWindow):
    model = None
    form_view = None

    def __init__(self, model=None):
        super().__init__()

        self.table_view = TableView(model or self.model)
        self.setCentralWidget(self.table_view)

        # -- RECORD TOOLBAR

        self.record_toolbar = RecordToolbar(self.table_view, self.form_view)
        self.addToolBar(Qt.TopToolBarArea, self.record_toolbar)

        self.add_record = self.record_toolbar.addAction(QIcon(':record/add'), 'Add record', self.record__add__click)
        self.edit_record = self.record_toolbar.addAction(QIcon(':record/edit'), 'Edit record', self.record__edit__click)
        self.delete_record = self.record_toolbar.addAction(QIcon(':record/delete'), 'Delete record', self.record__delete__click)

        # -- FILTER TOOLBAR

        # -- INFORMATION TOOLBAR

    def record__add__click(self, *args: typing.List[typing.Any], **kwargs: typing.Mapping) -> None:
        model = self.table.data_model
        record, model_index = model.add_record()

        self.open_form = self.form_view(self.table.data_model)
        self.open_form.set_record_index(model_index)
        self.open_form.show()

    def record__edit__click(self, *args: typing.List[typing.Any], **kwargs: typing.Mapping) -> None:
        model_index = self.table.get_selected_index()
        self.open_form = self.form_view(self.table.data_model)
        self.open_form.set_record_index(model_index)
        self.open_form.show()

    def record__delete__click(self, *args: typing.List[typing.Any], **kwargs: typing.Mapping) -> None:
        pass