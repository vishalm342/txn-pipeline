from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    txn_id = Column(String, nullable=True)
    date = Column(String, nullable=True)
    merchant = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    status = Column(String, nullable=True)
    category = Column(String, nullable=True)
    account_id = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    is_anomaly = Column(Boolean, default=False)
    anomaly_reason = Column(Text, nullable=True)

    llm_category = Column(String, nullable=True)
    llm_raw_response = Column(Text, nullable=True)
    llm_failed = Column(Boolean, default=False)