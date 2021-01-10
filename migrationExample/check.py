from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(f'postgresql://franziska:@localhost:5432/cc')

df = pd.read_sql_query("SELECT * FROM users",con=engine)


event = pd.DataFrame({'id':1, 'name':'anna'}, index=[0])
event.to_sql('users', engine, if_exists='append', index=False)

