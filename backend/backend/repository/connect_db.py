from sqlmodel import create_engine

def connect():
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/prueba-concepto")
    return engine

