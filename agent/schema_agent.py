from sqlalchemy import create_engine, inspect
from agent.config import DATABASE_PATH
import pandas as pd

class SchemaAgent:
    def __init__(self, db_path = DATABASE_PATH):
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.inspector = inspect(self.engine)


    def show_tables(self):
        return self.inspector.get_table_names()
    
    def describe_table(self, table_name):
        return self.inspector.get_columns(table_name)
    
    def fetch_table(self, table_name, limit = 5):
        query = f" Select * from {table_name} LIMIT {limit}"
        return pd.read_sql(query, con=self.engine)

    def generate_and_run_query(self, user_input):
        ''' 
            user_input is the insight that the user want from the database. for example total sales of each product in each day?
        '''
        
        


if __name__ == '__main__':
    agent = SchemaAgent()
    print("Tabels: ", agent.show_tables())

    for table in agent.show_tables():
        print(f"Schema for table {table}")
        print(agent.describe_table(table))
        print(f'Data Fetched from Table: {table}:')
        print(agent.fetch_table(table_name=table))
