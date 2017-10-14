from PyQt5.uic import loadUi
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget, QMainWindow, QDataWidgetMapper


class RecordFormView(QMainWindow):

    ui_file = ''  # type: str
    model = None

    def __init__(self, model=None, ui_file: str=None) -> None:
        super().__init__()
        loadUi(ui_file or self.ui_file, self)

        self.model = model or self.model

        self.data_mapper = QDataWidgetMapper()
        self.data_mapper.setModel(self.model)

        for field in model.fields:
            if hasattr(self, field.name):
                self.data_mapper.addMapping(getattr(self, field.name), field.index)

        if hasattr(self, 'setup_ui'):
            self.setup_ui()

    def set_record_index(self, index: QModelIndex) -> None:
        self.data_mapper.setCurrentModelIndex(index)