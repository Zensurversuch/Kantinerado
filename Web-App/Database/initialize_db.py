<<<<<<< HEAD
from dotenv import dotenv_values
import sys

sys.path.append("../Backend/DB_Repositories")
from models import initialize_database
=======
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, ARRAY, LargeBinary
from dotenv import dotenv_values

env_vars = dotenv_values("Development/Local-Environment/.env")

postgres_pw = env_vars.get("POSTGRES_PW")

# PostgreSQL connection string
POSTGRES_URL = f"postgresql://postgres:{postgres_pw}@localhost:5432/postgres"
>>>>>>> b9299c668f418c2016292c781b411c74c5594d12

env_vars = dotenv_values("../../Development/Local-Environment/.env")
postgres_pw = env_vars.get("POSTGRES_PW")

<<<<<<< HEAD
=======
    metadata = MetaData()

    # Define tables
    allergies = Table("allergies", metadata,
        Column("allergieID", Integer, primary_key=True),
        Column("name", String(50), nullable=False))

    dishes = Table("dishes", metadata,
        Column("dishID", Integer, primary_key=True),
        Column("name", String(50), nullable=False),
        Column("ingredients", ARRAY(String)),  # Assuming ingredients are stored as an array of strings
        Column("allergies", Integer, ForeignKey("allergies.allergieID"), nullable=True),
        Column("DietaryCategory", String(50), nullable=False),
        Column("MealType", String(50), nullable=False),
        Column("Image", LargeBinary))  # Change BINARY to BYTEA

    users = Table("users", metadata,
        Column("userID", Integer, primary_key=True),
        Column("email", String(50), nullable=False),
        Column("password", String(50), nullable=False),
        Column("lastName", String(50), nullable=False),
        Column("firstName", String(50), nullable=False),
        Column("role", String(50), nullable=False),
        Column("allergies", Integer, ForeignKey("allergies.allergieID"), nullable=True))

    orders = Table("orders", metadata,
        Column("orderID", Integer, primary_key=True),
        Column("userID", Integer, ForeignKey("users.userID"), nullable=False),
        Column("dishID", Integer, ForeignKey("dishes.dishID"), nullable=False),
        Column("amount", Integer, nullable=False),
        Column("orderDate", Date))

    meal_plan = Table("meal_plan", metadata,
        Column("mealPlanID", Integer, primary_key=True),
        Column("dishID", Integer, ForeignKey("dishes.dishID"), nullable=False),
        Column("date", Date, nullable=False))

    # Create tables
    metadata.create_all(engine)

    print("Datenbanktabellen wurden erfolgreich initialisiert.")
    
    engine.dispose()
    print("Datenbankverbindung wurde geschlossen.")
>>>>>>> b9299c668f418c2016292c781b411c74c5594d12

if __name__ == "__main__":
    initialize_database(postgres_pw)
