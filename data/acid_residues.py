import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class AcidResides(SqlAlchemyBase):
    __tablename__ = 'acid_resides'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    formula = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    degree_of_oxidation = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    acid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("acids.formula"), nullable=False)
    wiki = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    acids = orm.relationship('Acids')

    def __init__(self, data):
        self.formula = data[0]
        self.name = data[1]
        self.degree_of_oxidation = data[2]
        self.acid = data[3]
        self.wiki = data[4]
