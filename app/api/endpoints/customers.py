from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new customer.
    
    - **first_name**: Customer's first name (required)
    - **last_name**: Customer's last name (required)
    - **email**: Customer's email address (required, must be unique)
    - **phone**: Customer's phone number (required, minimum 10 digits)
    - **date_of_birth**: Customer's date of birth (required, cannot be in future)
    - **address**: Customer's address (required)
    - **city**: Customer's city (required)
    - **state**: Customer's state/province (required)
    - **postal_code**: Customer's postal code (required)
    - **country**: Customer's country (required)
    """
    return crud.CustomerCRUD.create_customer(db=db, customer_data=customer)


@router.get("/", response_model=schemas.CustomerListResponse)
def get_customers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search in name, email, or city"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of customers with pagination and filtering.
    
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 1000)
    - **search**: Search term to filter customers by name, email, or city
    - **is_active**: Filter by customer active status
    """
    customers, total = crud.CustomerCRUD.get_customers(
        db=db, 
        skip=skip, 
        limit=limit,
        search=search,
        is_active=is_active
    )
    
    return schemas.CustomerListResponse(
        customers=customers,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=len(customers)
    )


@router.get("/{customer_id}", response_model=schemas.CustomerWithEmploymentResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific customer by ID with their employment information.
    
    - **customer_id**: The ID of the customer to retrieve
    """
    customer = crud.CustomerCRUD.get_customer(db=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Get employment information
    employment = crud.EmploymentCRUD.get_employment_by_customer(db=db, customer_id=customer_id)
    
    return schemas.CustomerWithEmploymentResponse(
        **customer.__dict__,
        employment=employment
    )


@router.put("/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer(
    customer_id: int,
    customer_update: schemas.CustomerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a customer's information.
    
    - **customer_id**: The ID of the customer to update
    - **customer_update**: The fields to update (all fields are optional)
    """
    return crud.CustomerCRUD.update_customer(
        db=db, 
        customer_id=customer_id, 
        customer_data=customer_update
    )


@router.delete("/{customer_id}", response_model=schemas.MessageResponse)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """
    Soft delete a customer (sets is_active to False).
    
    - **customer_id**: The ID of the customer to delete
    """
    crud.CustomerCRUD.delete_customer(db=db, customer_id=customer_id)
    return schemas.MessageResponse(
        message=f"Customer with ID {customer_id} has been deactivated"
    )


@router.delete("/{customer_id}/hard", response_model=schemas.MessageResponse)
def hard_delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """
    Permanently delete a customer and all associated data.
    
    - **customer_id**: The ID of the customer to permanently delete
    """
    crud.CustomerCRUD.hard_delete_customer(db=db, customer_id=customer_id)
    return schemas.MessageResponse(
        message=f"Customer with ID {customer_id} has been permanently deleted"
    )


@router.get("/email/{email}", response_model=schemas.CustomerWithEmploymentResponse)
def get_customer_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a customer by email address.
    
    - **email**: The email address of the customer to retrieve
    """
    customer = crud.CustomerCRUD.get_customer_by_email(db=db, email=email)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Get employment information
    employment = crud.EmploymentCRUD.get_employment_by_customer(db=db, customer_id=customer.id)
    
    return schemas.CustomerWithEmploymentResponse(
        **customer.__dict__,
        employment=employment
    ) 