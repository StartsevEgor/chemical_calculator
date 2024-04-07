import sqlalchemy
from .db_session import SqlAlchemyBase


class Acids(SqlAlchemyBase):
    __tablename__ = 'acids'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    formula = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    wiki = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __init__(self, data):
        self.formula = data[0]
        self.name = data[1]
        self.wiki = data[2]