from sqlalchemy import (Column, Date, Text, SmallInteger, Integer)
from sqlalchemy.orm import relationship

class NutritionistReview():
    __tablename__ = 'nutritionist_review'
    id = Column(Integer, primary_key=True)

    nutritionist_id = relationship("Nutritionist")
    user_id = relationship("User")
    text = Column(Text)
    rating = Column(SmallInteger)
    
    created_date = Column(Date)
    updated_date = Column(Date)
