from ..model.user_model import User
from .connect_db import connect
from sqlmodel import Session, select


def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(User)
        return session.exec(query).all()
    

def select_user_by_email(email: str):
    engine = connect()
    with Session(engine) as session:
        query = select(User).where(User.username == email) 
        return session.exec(query).all()
    