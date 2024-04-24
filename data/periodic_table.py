import sqlalchemy
from .db_session import SqlAlchemyBase


class PeriodicTable(SqlAlchemyBase):
    __tablename__ = 'periodic_table'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    formula = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    group = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    period = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_metal = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    electronegativity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    wiki = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __init__(self, data):
        self.formula = data[0]
        self.name = data[1]
        self.number = data[2]
        self.group = data[3]
        self.period = data[4]
        self.is_metal = data[5]
        self.type = data[6]
        self.electronegativity = data[7]
        self.wiki = data[8]

    def __str__(self):
        return self.formula
