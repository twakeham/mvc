import typing

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QMessageBox


class RecordToolbar(QToolBar):

    def __init__(self, table, form) -> None:
        super().__init__('Record')

        self.table = table
        self.form_view = form
        self.open_form = None

        self.add_record = self.addAction(QIcon(':record/add'), 'Add record', self.add_record__click)
        self.edit_record = self.addAction(QIcon(':record/edit'), 'Edit record', self.edit_record__click)
        self.delete_record = self.addAction(QIcon(':record/delete'), 'Delete record', self.delete_record__click)

    def add_record__click(self, *args: typing.List[typing.Any], **kwargs: typing.Mapping) -> None:
        model = self.table.data_model
        record, model_index = model.add_record()

        self.open_form = self.form_view(self.table.data_model)
        self.open_form.set_record_index(model_index)
        self.open_form.show()

    def edit_record__click(self, *args: typing.List[typing.Any], **kwargs: typing.Mapping) -> None:
        model_index = self.table.get_selected_index()
        self.open_form = self.form_view(self.table.data_model)
        self.open_form.set_record_index(model_index)
        self.open_form.show()

    def delete_record__click(self, *args: typing.List[typing.Any], **kwargs: typing.Mapping) -> None:
        pass
