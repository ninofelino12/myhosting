from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker
import yaml

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'app'

   
    key = Column(String(255),primary_key=True)
    name = Column(String(255))
    data = Column(String(255))
    yaml = Column(String(255))

engine = create_engine('sqlite:///database.db')   
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


users = session.query(User).all()
with open('app.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

for record in yaml_data.items():
    user = User(key="sss",name='data',data='data',yaml="ya")
    session.add(user)
session.commit()

