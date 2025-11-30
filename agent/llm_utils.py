from agent.config import MODEL_PATH
from gpt4all import GPT4All
import re
import warnings
warnings.filterwarnings("ignore")


def extract_sql(text: str) -> str:
    match = re.search(r"\*\*\*(.*?)\*\*\*", text, re.DOTALL)
    return match.group(1)



model = GPT4All(
    model_name='llama3-8b-instruct-Q5_K_M.gguf',
    model_path=MODEL_PATH)
print('model loaded successfully!')

user_request = "Find the total sales per product from table `order_table`."

prompt = f'''
            You are an SQL generator.
            Task: Output ONLY a single valid SQLite query for the user's request.
            Rules:
            1. Wrap the SQL query between triple asterisks: ***SQL_QUERY***.
            2. Do not include explanations, code blocks, comments, or any extra text outside the asterisks.
            3. Output must be a single line.
            4. Do not output multiple SQL queries, only one.
            5. Do not use SQL functions unsupported by SQLite.
            6. Do not include placeholders or examples, only the final SQL.

            User request: {user_request}
            '''

sql_output = model.generate(prompt)
print("Sample output:", extract_sql(sql_output))

