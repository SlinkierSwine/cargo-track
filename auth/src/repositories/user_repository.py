from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from entities.user import User, UserCreate, UserUpdate
from entities.database_models import UserModel
from repositories.interfaces.user_repository import IUserRepository
from utils.password_utils import hash_password


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, user_data: UserCreate) -> User:
        hashed_password = hash_password(user_data.password)
        
        db_user = UserModel(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            role=user_data.role,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            is_active=db_user.is_active,
            first_name=db_user.first_name,
            last_name=db_user.last_name
        )
    
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        db_user = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not db_user:
            return None
            
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            is_active=db_user.is_active,
            first_name=db_user.first_name,
            last_name=db_user.last_name
        )
    
    def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.session.query(UserModel).filter(UserModel.email == email).first()
        
        if not db_user:
            return None
            
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            is_active=db_user.is_active,
            first_name=db_user.first_name,
            last_name=db_user.last_name
        )
    
    def get_by_username(self, username: str) -> Optional[User]:
        db_user = self.session.query(UserModel).filter(UserModel.username == username).first()
        
        if not db_user:
            return None
            
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            is_active=db_user.is_active,
            first_name=db_user.first_name,
            last_name=db_user.last_name
        )
    
    def update(self, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        db_user = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not db_user:
            return None
        
        if user_data.email is not None:
            db_user.email = user_data.email
        if user_data.username is not None:
            db_user.username = user_data.username
        if user_data.role is not None:
            db_user.role = user_data.role
        if user_data.is_active is not None:
            db_user.is_active = user_data.is_active
        if user_data.first_name is not None:
            db_user.first_name = user_data.first_name
        if user_data.last_name is not None:
            db_user.last_name = user_data.last_name
        
        self.session.commit()
        self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            is_active=db_user.is_active,
            first_name=db_user.first_name,
            last_name=db_user.last_name
        )
    
    def delete(self, user_id: UUID) -> bool:
        db_user = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False
        
        self.session.delete(db_user)
        self.session.commit()
        return True
    
    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        db_users = self.session.query(UserModel).offset(skip).limit(limit).all()
        
        return [
            User(
                id=db_user.id,
                email=db_user.email,
                username=db_user.username,
                hashed_password=db_user.hashed_password,
                role=db_user.role,
                is_active=db_user.is_active,
                first_name=db_user.first_name,
                last_name=db_user.last_name
            )
            for db_user in db_users
        ] 