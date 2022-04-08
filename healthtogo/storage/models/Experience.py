from sqlalchemy import (Integer, Column, String)

class Experience():
    __tablename__ = 'experience'
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
