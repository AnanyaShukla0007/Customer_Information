from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from app import models, schemas
from fastapi import HTTPException, status


class CustomerCRUD:
    @staticmethod
    def create_customer(db: Session, customer_data: schemas.CustomerCreate) -> models.Customer:
        # Check if email already exists
        existing_customer = db.query(models.Customer).filter(
            models.Customer.email == customer_data.email
        ).first()
        
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        db_customer = models.Customer(**customer_data.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
        return db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    
    @staticmethod
    def get_customer_by_email(db: Session, email: str) -> Optional[models.Customer]:
        return db.query(models.Customer).filter(models.Customer.email == email).first()
    
    @staticmethod
    def get_customers(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> tuple[List[models.Customer], int]:
        query = db.query(models.Customer)
        
        # Apply filters
        if search:
            search_filter = or_(
                models.Customer.first_name.ilike(f"%{search}%"),
                models.Customer.last_name.ilike(f"%{search}%"),
                models.Customer.email.ilike(f"%{search}%"),
                models.Customer.city.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if is_active is not None:
            query = query.filter(models.Customer.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        customers = query.offset(skip).limit(limit).all()
        
        return customers, total
    
    @staticmethod
    def update_customer(
        db: Session, 
        customer_id: int, 
        customer_data: schemas.CustomerUpdate
    ) -> Optional[models.Customer]:
        db_customer = CustomerCRUD.get_customer(db, customer_id)
        if not db_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Check if email is being updated and if it already exists
        if customer_data.email and customer_data.email != db_customer.email:
            existing_customer = CustomerCRUD.get_customer_by_email(db, customer_data.email)
            if existing_customer:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Update only provided fields
        update_data = customer_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> bool:
        db_customer = CustomerCRUD.get_customer(db, customer_id)
        if not db_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Soft delete - set is_active to False
        db_customer.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def hard_delete_customer(db: Session, customer_id: int) -> bool:
        db_customer = CustomerCRUD.get_customer(db, customer_id)
        if not db_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        db.delete(db_customer)
        db.commit()
        return True


class EmploymentCRUD:
    @staticmethod
    def create_employment(
        db: Session, 
        customer_id: int, 
        employment_data: schemas.EmploymentCreate
    ) -> models.Employment:
        # Check if customer exists
        customer = CustomerCRUD.get_customer(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Check if customer already has employment
        existing_employment = db.query(models.Employment).filter(
            models.Employment.customer_id == customer_id
        ).first()
        
        if existing_employment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer already has employment information"
            )
        
        db_employment = models.Employment(
            customer_id=customer_id,
            **employment_data.dict()
        )
        db.add(db_employment)
        db.commit()
        db.refresh(db_employment)
        return db_employment
    
    @staticmethod
    def get_employment(db: Session, employment_id: int) -> Optional[models.Employment]:
        return db.query(models.Employment).filter(models.Employment.id == employment_id).first()
    
    @staticmethod
    def get_employment_by_customer(db: Session, customer_id: int) -> Optional[models.Employment]:
        return db.query(models.Employment).filter(models.Employment.customer_id == customer_id).first()
    
    @staticmethod
    def get_employments(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        employment_type: Optional[str] = None,
        is_current: Optional[bool] = None
    ) -> tuple[List[models.Employment], int]:
        query = db.query(models.Employment)
        
        # Apply filters
        if search:
            search_filter = or_(
                models.Employment.company_name.ilike(f"%{search}%"),
                models.Employment.job_title.ilike(f"%{search}%"),
                models.Employment.department.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if employment_type:
            query = query.filter(models.Employment.employment_type == employment_type)
        
        if is_current is not None:
            query = query.filter(models.Employment.is_current_employment == is_current)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        employments = query.offset(skip).limit(limit).all()
        
        return employments, total
    
    @staticmethod
    def update_employment(
        db: Session, 
        employment_id: int, 
        employment_data: schemas.EmploymentUpdate
    ) -> Optional[models.Employment]:
        db_employment = EmploymentCRUD.get_employment(db, employment_id)
        if not db_employment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employment not found"
            )
        
        # Update only provided fields
        update_data = employment_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_employment, field, value)
        
        db.commit()
        db.refresh(db_employment)
        return db_employment
    
    @staticmethod
    def delete_employment(db: Session, employment_id: int) -> bool:
        db_employment = EmploymentCRUD.get_employment(db, employment_id)
        if not db_employment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employment not found"
            )
        
        db.delete(db_employment)
        db.commit()
        return True


class CustomerRegistrationCRUD:
    @staticmethod
    def create_customer_with_employment(
        db: Session, 
        registration_data: schemas.CustomerRegistration
    ) -> tuple[models.Customer, models.Employment]:
        # Create customer first
        customer = CustomerCRUD.create_customer(db, registration_data.customer)
        
        # Create employment
        employment = EmploymentCRUD.create_employment(
            db, 
            customer.id, 
            registration_data.employment
        )
        
        return customer, employment 