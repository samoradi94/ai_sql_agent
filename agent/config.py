import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))

DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'analytics.db')

print(DATABASE_PATH)


