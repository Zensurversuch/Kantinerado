from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, Date
from sqlalchemy.ext.declarative import declarative_base


class OrderRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)