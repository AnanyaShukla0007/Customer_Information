from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=False)
    country = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with employment
    employment = relationship("Employment", back_populates="customer", uselist=False)


class Employment(Base):
    __tablename__ = "employments"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    company_name = Column(String(100), nullable=False)
    job_title = Column(String(100), nullable=False)
    department = Column(String(100))
    employment_type = Column(String(50), nullable=False)  # Full-time, Part-time, Contract, etc.
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Null if currently employed
    salary = Column(String(50))
    work_address = Column(Text)
    work_city = Column(String(50))
    work_state = Column(String(50))
    work_postal_code = Column(String(10))
    work_country = Column(String(50))
    is_current_employment = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with customer
    customer = relationship("Customer", back_populates="employment") 