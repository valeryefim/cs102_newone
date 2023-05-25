import sqlalchemy  # type: ignore
from sqlalchemy import Column, Integer, String, create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

Base = sqlalchemy.orm.declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)
