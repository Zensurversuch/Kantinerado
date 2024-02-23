from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    userID = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    lastName = Column(String)
    firstName = Column(String)
    role = Column(String)
    allergies = Column(Integer)

class UserRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)

    def create_user(self, email, password, lastName, firstName, role, allergies=None):
        try:
            session = scoped_session(self.session_factory)
            new_user = User(email=email, password=password, lastName=lastName, firstName=firstName, role=role, allergies=allergies)
            session.add(new_user)
            session.commit()
            return True
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    def get_all_users(self):
        try:
            session = scoped_session(self.session_factory)
            all_users = session.query(User).all()
            return all_users
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    def get_user_by_id(self, user_id):
        try:
            session = scoped_session(self.session_factory)
            user_data = session.query(User).filter(User.userID == user_id).first()
            if user_data:
                user_dict = {
                    'userID': user_data.userID,
                    'email': user_data.email,
                    'lastName': user_data.lastName,
                    'firstName': user_data.firstName,
                    'role': user_data.role,
                    'allergies': user_data.allergies
                }
                return user_dict
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()


    def get_password_for_user(self, user_id):
        try:
            session = scoped_session(self.session_factory)
            user_pw = session.query(User.password).filter(User.userID == user_id).scalar()
            return user_pw
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()