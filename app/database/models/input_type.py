from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from models import Base


class InputType(Base):
    __tablename__ = 'input_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    problems = relationship("Problem", back_populates="input_type")

    def __repr__(self):
        return f"<InputType(id={self.id}, name='{self.name}')>"
