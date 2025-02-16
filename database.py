from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app_name = "UPIITAExpediente" 
app_data_path = os.path.join(os.getenv("LOCALAPPDATA"), app_name)
os.makedirs(app_data_path, exist_ok=True)  # Crea el folder si no existe

DATABASE_PATH = os.path.join(app_data_path, "database.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def obtener_sesion():
    return SessionLocal()
