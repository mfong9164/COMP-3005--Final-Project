from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import base

DB_USER = 'postgres'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'Health and Fitness Club Management System'

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def main():
    try:
        with engine.connect() as conn:
            print("Connected")
    except Exception as e:
        print(f"Failed: ")
        return

    Base.metadata.create_all(engine, checkfirst=True)

    with Session(engine) as session:
        pass

if __name__ == '__main__':
    main()