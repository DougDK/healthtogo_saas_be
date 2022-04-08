from sqlalchemy import (Integer, Column)
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import relationship

class Agenda():
    __tablename__ = 'agenda'
    id = Column(Integer, primary_key=True)

    nutritionist_id = relationship("Nutritionist")
    availability = Column(JSONB)
