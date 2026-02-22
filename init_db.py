from db import engine, Base
from models import Card

Base.metadata.create_all(engine)
print("Tables created.")