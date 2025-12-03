from agent.config import MODEL_PATH
from agent.schema_agent import SchemaAgent
from gpt4all import GPT4All
import re
import mlflow
from mlflow import log_param, log_metric, log_text
import time
import warnings
warnings.filterwarnings("ignore")


def extract_sql(text: str) -> str:
    match = re.search(r"\*\*\*(.*?)\*\*\*", text, re.DOTALL)
    return match.group(1)


def log_llm_request(user_request, keywords_output, model_name, duration):
    mlflow.set_experiment('llm_sql_agent')

    with mlflow.start_run():
        log_param("user_request", user_request)
        log_param("model_name", model_name)

        log_metric("output_length", len(keywords_output))
        log_metric("duration", duration)

        log_text(keywords_output, "model_output.txt")

model_name='llama3-8b-instruct-Q5_K_M.gguf'
model = GPT4All(
    model_name='llama3-8b-instruct-Q5_K_M.gguf',
    model_path=MODEL_PATH)
print('model loaded successfully!')

user_request = "Find the total sales per product from table `order_table`."
# user_request = "از جدول order_table مجموع فروش به ازای هر محصول را بده"
# todo: for next stable version we will work on user input in Farsi 

schema_agent = SchemaAgent()
tables = schema_agent.show_tables()

tables_info = {}
if len(tables) < 10:
    for table in tables:
        tables_info[table] = schema_agent.describe_table(table)
if True:
    prompt_2 = f"""
               You are a data assistant.
                Follow the rules strictly:

                Extract only database-related keywords (table names, column names, metrics).

                Output only the extracted keywords as a comma-separated list.

                Do not output explanations, sentences, code, comments, translations, or anything except the keyword list.

                Do not generate Python code under any circumstance.

                The final answer must be only the keyword list.

                User request: {user_request}

                """
    start = time.time()
    keywords_output = model.generate(prompt_2)
    duration = time.time() - start

    log_llm_request(user_request= user_request,
                    keywords_output=keywords_output,
                    model_name= model_name,
                    duration=duration)
    print(keywords_output.strip())


# print(tables_info)

exit()

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
