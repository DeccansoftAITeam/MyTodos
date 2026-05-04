import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

odbc_conn = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=.\\sqlexpress;"
    "DATABASE=myclaudetodo;"
    "Trusted_Connection=yes;"
)
DATABASE_URL = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(odbc_conn)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
