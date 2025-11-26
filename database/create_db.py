import pandas as pd
from sqlalchemy import create_engine


df = pd.read_csv('./data/raw/sample.csv')

engine = create_engine('sqlite:///database/analytics.db')

df.to_sql('order_table', con= engine, if_exists='replace', index=False)

print('database created successfully!!')

# df_from_db = pd.read_sql('select * from order_table', engine)
# print(df_from_db)
