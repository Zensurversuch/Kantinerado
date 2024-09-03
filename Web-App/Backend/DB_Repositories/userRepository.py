from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from DB_Repositories.models import User, Allergy
from random import randint 
import secrets
import hashlib

class UserRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)

    def create_user(self, param_email, param_password, param_lastName, param_firstName, param_role, param_allergies=None):
        session = scoped_session(self.session_factory)
        try:
            min_ = 1
            max_ = 1000000000
            rand_userid = randint(min_, max_)
            while session.query(User).filter(User.userID == rand_userid).first() is not None:
                rand_userid = randint(min_, max_)

            salt = secrets.token_hex()
            hashed_pw = hashlib.sha256((param_password + salt).encode('utf-8')).hexdigest()
            new_user = User(userID=rand_userid,
                            email=param_email,
                            password=hashed_pw,
                            lastName=param_lastName,
                            firstName=param_firstName,
                            role=param_role,
                            salt = salt)

            missing_allergies = []
            if param_allergies:
                for allergy_name in param_allergies:
                    allergy = session.query(Allergy).filter(Allergy.name == allergy_name).first()
                    if allergy:
                        new_user.allergies.append(allergy)
                    else:
                        missing_allergies.append(allergy_name)

            session.add(new_user)
            session.commit()

            return missing_allergies
        except SQLAlchemyError as e:
            return False
        finally:
            session.close()


    def get_all_users(self):
        try:
            session = scoped_session(self.session_factory)
            all_users = session.query(User).all()
            user_list = []

            if all_users:
                for user in all_users:
                    allergies = [allergy.name for allergy in user.allergies] if user.allergies else None
                    user_dict = {
                        "userID": user.userID,
                        "email": user.email,
                        "lastName": user.lastName,
                        "firstName": user.firstName,
                        "role": user.role,
                        "allergies": allergies
                    }
                    user_list.append(user_dict)

                return user_list
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    def get_user_by_id(self, param_userID):
        try:
            session = scoped_session(self.session_factory)
            user_data = session.query(User).filter(User.userID == param_userID).first()
            if user_data:
                allergies = [allergy.name for allergy in user_data.allergies] if user_data.allergies else None

                user_dict = {
                    "userID": user_data.userID,
                    "email": user_data.email,
                    "lastName": user_data.lastName,
                    "firstName": user_data.firstName,
                    "role": user_data.role,
                    "allergies": allergies
                }
                return user_dict
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    def get_user_by_email(self, param_email):
        try:
            session = scoped_session(self.session_factory)
            user_data = session.query(User).filter(User.email == param_email).first()
            if user_data:
                allergies = [allergy.name for allergy in user_data.allergies] if user_data.allergies else None

                user_dict = {
                    "userID": user_data.userID,
                    "password": user_data.password,
                    "email": user_data.email,
                    "lastName": user_data.lastName,
                    "firstName": user_data.firstName,
                    "role": user_data.role,
                    "salt": user_data.salt,
                    "allergies": allergies
                }
                return user_dict
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    
    def set_user_allergies_by_id(self, param_id, param_allergies):
        session = scoped_session(self.session_factory)
        try:
            user = session.query(User).filter(User.userID == param_id).first()
            if user: 
                user.allergies = []
                session.commit()

                missing_allergies = []
                if param_allergies:
                    for allergy_name in param_allergies:
                        allergy = session.query(Allergy).filter(Allergy.name == allergy_name).first()
                        if allergy:
                            user.allergies.append(allergy)
                        else:
                            missing_allergies.append(allergy_name)

                session.commit()
            else:
                return "User not found!"
        
            return missing_allergies
        except SQLAlchemyError as e:
            session.rollback()
            return False
        finally:
            session.close()