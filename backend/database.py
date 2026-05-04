import os
import urllib
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


def _resolve_driver() -> str:
    explicit = os.getenv("ODBC_DRIVER")
    if explicit:
        return explicit
    sql_drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
    if sql_drivers:
        return sql_drivers[-1]
    return "ODBC Driver 17 for SQL Server"


SERVER = os.getenv("DB_SERVER", ".\\sqlexpress")
DATABASE = os.getenv("DB_NAME", "myclaudetodo")
DRIVER = _resolve_driver()

odbc_conn = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
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
