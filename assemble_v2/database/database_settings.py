import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection parameters
DB_HOST = "localhost"
DB_USER = "MickelUWE"
DB_PASSWORD = "g<bI1Z11iC]c"
DB_NAME = "Cinema"

# MySQL Connector connection
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# SQLAlchemy configuration
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME.lower()}"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_db_connection():
    """
    Creates and returns a fresh MySQL connector connection
    """
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def get_db():
    """
    Creates and returns a new SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()