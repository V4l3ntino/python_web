from sqlmodel import create_engine

def connect():
    engine = create_engine("mysql+pymysql://root:@localhost:3306/product")
    return engine