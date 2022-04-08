from sqlalchemy import (Integer, Column, String)

class Expertise():
    __tablename__ = 'expertise'
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
