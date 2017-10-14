import sys

from PyQt5.QtWidgets import QApplication, QPushButton

from utils.events import EventConnector

app = QApplication([])

from assets import resources


from PyQt5.QtSql import QSqlDatabase


application = QApplication(sys.argv)
#application.setStyle('Fusion')

database = QSqlDatabase.addDatabase('QPSQL')
database.setHostName('203.31.49.113')
database.setDatabaseName('transport')
database.setUserName('postgres')
database.setPassword('postgres')
print(database.open())


from db.model import DatabaseModel
from views.record_table import RecordTableView
from views.record_form import RecordFormView


class OrderModel(DatabaseModel):
    table = 'orders'
    auto_populate_id = True
    id_field_name = 'id'
    id_sequence_name = 'order_ids'

    def __init__(self):
        super().__init__()

        self.id.header = 'ID'


model = OrderModel()
model.select()


class FormView(RecordFormView):
    model = model
    ui_file = 'order.ui'


class TableView(RecordTableView):
    model = model
    form_view = FormView


table_view = TableView()
table_view.show()

#form = RecordFormView(model, 'order.ui')
#form.show()



sys.exit(app.exec_())

