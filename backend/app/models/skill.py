from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, index=True, nullable=False)
    level = Column(Integer, nullable=False)  # 0–100

    category = Column(String)  
    # strong | average | missing

    user = relationship("User", backref="skills")
