from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from const_config import engine_URL

engine = create_engine(engine_URL)
Session = sessionmaker(engine, echo=True)
