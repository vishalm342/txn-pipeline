from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey
from app.db.base import Base


class JobSummary(Base):
    __tablename__ = "job_summaries"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    total_spend_inr = Column(Float, nullable=True)
    total_spend_usd = Column(Float, nullable=True)
    top_merchants = Column(Text, nullable=True)
    anomaly_count = Column(Integer, nullable=True)
    narrative = Column(Text, nullable=True)
    risk_level = Column(String, nullable=True)