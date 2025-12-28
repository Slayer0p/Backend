from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)

    # Relations
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Tracking data
    skill = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False)  
    # started | in-progress | completed

    hours_spent = Column(Integer, default=0)
    progress_percent = Column(Integer, default=0)  # 0–100

    date = Column(Date, nullable=False)

    # ORM relation (optional but powerful)
    user = relationship("User", backref="progress_entries")
