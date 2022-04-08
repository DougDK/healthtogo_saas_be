from sqlalchemy import (Integer, Column, Date)
from sqlalchemy.orm import relationship

class MedicalAppointment():
    __tablename__ = 'medical_appointment'
    id = Column(Integer, primary_key=True)

    nutritionist_id = relationship("Nutritionist")
    user_id = relationship("User")
    
    medical_appointment_date = Column(Date)
    created_date = Column(Date)
    updated_date = Column(Date)
