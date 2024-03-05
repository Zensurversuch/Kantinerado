from dotenv import dotenv_values
import sys

sys.path.append("../Backend/DB_Repositories")
from models import initialize_database

env_vars = dotenv_values("../../Development/Local-Environment/.env")
postgres_pw = env_vars.get("POSTGRES_PW")


if __name__ == "__main__":
    initialize_database(postgres_pw, "localhost")
