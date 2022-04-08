from sqlalchemy import (Integer, Column, String)

class Education():
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)

    school = Column(String(255))
    degree = Column(String(255))
    field_of_study = Column(String(255))
