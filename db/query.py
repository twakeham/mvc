from PyQt5.QtSql import QSqlQuery


class SqlCalculation:
    query = ''
    parameters = []

    def check_args(self, **kwargs):
        for parameter in self.parameters:
            if parameter not in kwargs:
                return False
        return True

    def calculate(self, **kwargs):
        if not self.check_args(**kwargs):
            raise KeyError('Missing arguments - requires {0}'.format(','.join(self.parameters)))
        sql_query = QSqlQuery(self.query.format(**kwargs))
        sql_query.next()
        return sql_query.value(0) or 0