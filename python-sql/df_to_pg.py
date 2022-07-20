import os

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, MetaData

load_dotenv(".env")

CONNECTION_STRING = os.environ.get('DATABASE_URL')
DATA_PATH = 'data/calendar.csv'


def main():
    try:

        engine = create_engine(CONNECTION_STRING)
        metadata = MetaData()

        df = pd.read_csv(DATA_PATH)

        print(len(df.index))

        df.to_sql('airbnb_calendar', engine)

        print("Successful Loading")
        
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
