import typing

from PyQt5.Qt import pyqtSignal
from PyQt5.QtCore import Qt, QModelIndex, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtSql import QSqlTableModel, QSqlRecord, QSqlQuery

from exceptions import ImproperlyConfigured
from utils.events import EventConnector


class DatabaseField(QObject):

    def __init__(self, name: str, index: int):
        super().__init__()
        self.name = name
        self.header = ' '.join([part.title() for part in name.split('_')])
        self.index = index
        self.validation = None

    def display(self, value, record: QSqlRecord) -> str:
        return value

    def text_colour(self, value, record: QSqlRecord) -> QColor:
        return None

    def background_colour(self, value, record: QSqlRecord) -> QColor:
        return None

    def flags(self, value, record: QSqlRecord) -> int:
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class DatabaseModel(QSqlTableModel, EventConnector):
    table = ''

    auto_populate_id = True  # type: bool
    id_field_name = 'id'  # type: str
    id_sequence_name = ''  # type: str

    def __init__(self) -> None:
        super().__init__()

        self.setTable(self.table)

        record = self.record()

        if self.auto_populate_id:
            if not (self.id_sequence_name and self.id_field_name) :
                raise ImproperlyConfigured('id_sequence_name must be provided if auto_populate_id is set')

        self.fields = [] # type: List[DatabaseField]

        for column_idx in range(self.columnCount()):
            field_name = record.fieldName(column_idx)
            field = DatabaseField(field_name, column_idx)
            self.fields.append(field)
            setattr(self, field_name, field)

        EventConnector.connect(self)

    def headerData(self, index: int, orientation: int, role: int=None) -> str:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.fields[index].header

    def data(self, model_index: QModelIndex, role: int=None):
        if not model_index.isValid():
            return None

        if role not in [Qt.DisplayRole, Qt.ForegroundRole, Qt.BackgroundRole]:
            return super().data(model_index, role)

        row = model_index.row()
        record = super().record(row)
        column = model_index.column()
        field = self.fields[column]
        field_value = record.value(field.index)

        if role == Qt.DisplayRole:
            return field.display(field_value, record)

        elif role == Qt.ForegroundRole:
            return field.text_colour(field_value, record)

        elif role == Qt.BackgroundRole:
            return field.background_colour(field_value, record)

        else:
            return None

    def flags(self, model_index: QModelIndex) -> int:
        row = model_index.row()
        record = super().record(row)
        column = model_index.column()
        field = self.fields[column]
        field_value = record.value(field.index)

        return field.flags(field_value, record)

    def get_auto_populated_id(self):
        query = QSqlQuery("SELECT nextval('{0}')".format(self.id_sequence_name))
        query.next()
        return query.value(0)

    def add_record(self):
        row_count = self.rowCount()
        self.insertRow(row_count)
        model_index = self.index(row_count, 0)
        record = self.record(row_count)

        if self.auto_populate_id:
            id_field_index = self.record().indexOf(self.id_field_name)
            id_model_index = self.index(row_count, id_field_index)
            id_value = self.get_auto_populated_id()
            self.setData(id_model_index, id_value, Qt.EditRole)

        return record, model_index


class RelatedDatabaseModel(DatabaseModel):
    id_field = 'id'

    def set_related_id(self, related_id: typing.Union[str, int]) -> None:
        # quote string ids
        if type(related_id) is str:
            related_id = '"{0}"'.format(related_id)
        self.setFilter('{0}={1}'.format(self.id_field, related_id))




