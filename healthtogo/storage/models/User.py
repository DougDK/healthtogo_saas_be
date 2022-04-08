from sqlalchemy import (Integer, Column, String)
from sqlalchemy.orm import relationship

class User():
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    telephone = Column(String)
    picture_src = Column(String)

    review = relationship("NutritionistReview")
    medical_appointment = relationship("MedicalAppointment")