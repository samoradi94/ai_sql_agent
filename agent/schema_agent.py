from sqlalchemy import create_engine, inspect
from agent.config import DATABASE_PATH

class SchemaAgent:
    def __init__(self, db_path = DATABASE_PATH):
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.inspector = inspect(self.engine)


    def show_tables(self):
        return self.inspector.get_table_names()
    
    def describe_table(self, table_name):
        return self.inspector.get_columns(table_name)

        
        


if __name__ == '__main__':
    agent = SchemaAgent()
    print("Tabels: ", agent.show_tables())

    for table in agent.show_tables():
        print(f"Schema for table {table}")
        print(agent.describe_table(table))
