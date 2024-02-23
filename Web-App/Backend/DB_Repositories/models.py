from sqlalchemy import create_engine, MetaData, Column, Integer, String, Date, Table, ForeignKey, ARRAY, LargeBinary
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

# n-m user allergy
user_allergy_association = Table(
    'user_allergy_association', Base.metadata,
    Column('userId', Integer, ForeignKey('users.userID')),
    Column('allergyId', Integer, ForeignKey('allergies.allergieID'))
)

# n-m dish allergy
dish_allergy_association = Table(
    'dish_allergy_association', Base.metadata,
    Column('dishId', Integer, ForeignKey('dishes.dishID')),
    Column('allergyId', Integer, ForeignKey('allergies.allergieID'))
)

class Allergy(Base):
    __tablename__ = 'allergies'

    allergieID = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Dish(Base):
    __tablename__ = 'dishes'

    dishID = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    ingredients = Column(ARRAY(String))
    dietaryCategory = Column(String(50), nullable=False)
    mealType = Column(String(50), nullable=False)
    image = Column(LargeBinary)
    
    # n-m to allergy
    allergies = relationship("Allergy", secondary=dish_allergy_association)

class User(Base):
    __tablename__ = 'users'

    userID = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    
    # n-m to allergy
    allergies = relationship("Allergy", secondary=user_allergy_association)

class Order(Base):
    __tablename__ = 'orders'

    orderID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    dishID = Column(Integer, ForeignKey('dishes.dishID'), nullable=False)
    amount = Column(Integer, nullable=False)
    orderDate = Column(Date)

class MealPlan(Base):
    __tablename__ = 'mealPlan'

    mealPlanID = Column(Integer, primary_key=True)
    dishID = Column(Integer, ForeignKey('dishes.dishID'), nullable=False)
    date = Column(Date, nullable=False)

def initialize_database(postgres_pw):    
    POSTGRES_URL = f"postgresql://postgres:{postgres_pw}@localhost:5432/postgres"
    engine = create_engine(POSTGRES_URL)
    
    Base.metadata.create_all(engine)
    print("Datenbanktabellen wurden erfolgreich initialisiert.")