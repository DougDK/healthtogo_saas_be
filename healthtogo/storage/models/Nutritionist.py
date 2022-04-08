from sqlalchemy import (Integer, Column, SmallInteger, String, Text)
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import relationship

class Nutritionist():
    __tablename__ = 'nutritionist'
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    telephone = Column(String)
    picture_src = Column(String)

    crn = Column(String)
    description = Column(Text)
    expertise = Column(JSONB)
    experiencie = Column(JSONB)
    education = Column(JSONB)
    medical_appt_procedure = Column(Text)
    
    city = Column(String)
    state = Column(String)
    street_address = Column(String)
    street_number = Column(Integer)
    postal_code = Column(String)
    additional_address = Column(String)

    rating = Column(SmallInteger)
    review_qty = Column(Integer)
    review = relationship("NutritionistReview")

    agenda = relationship("Agenda")
    medical_appointment = relationship("MedicalAppointment")