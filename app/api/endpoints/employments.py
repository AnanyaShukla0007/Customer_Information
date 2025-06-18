from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.EmploymentResponse, status_code=status.HTTP_201_CREATED)
def create_employment(
    customer_id: int,
    employment: schemas.EmploymentCreate,
    db: Session = Depends(get_db)
):
    """
    Create employment information for a customer.
    
    - **customer_id**: The ID of the customer
    - **company_name**: Name of the company (required)
    - **job_title**: Job title/position (required)
    - **department**: Department (optional)
    - **employment_type**: Type of employment (Full-time, Part-time, etc.)
    - **start_date**: Employment start date (required)
    - **end_date**: Employment end date (optional, for past employments)
    - **salary**: Salary information (optional)
    - **work_address**: Work address (optional)
    - **work_city**: Work city (optional)
    - **work_state**: Work state/province (optional)
    - **work_postal_code**: Work postal code (optional)
    - **work_country**: Work country (optional)
    - **is_current_employment**: Whether this is current employment (default: True)
    """
    return crud.EmploymentCRUD.create_employment(
        db=db, 
        customer_id=customer_id, 
        employment_data=employment
    )


@router.get("/", response_model=schemas.EmploymentListResponse)
def get_employments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search in company name, job title, or department"),
    employment_type: Optional[str] = Query(None, description="Filter by employment type"),
    is_current: Optional[bool] = Query(None, description="Filter by current employment status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of employments with pagination and filtering.
    
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 1000)
    - **search**: Search term to filter employments by company, job title, or department
    - **employment_type**: Filter by employment type
    - **is_current**: Filter by current employment status
    """
    employments, total = crud.EmploymentCRUD.get_employments(
        db=db, 
        skip=skip, 
        limit=limit,
        search=search,
        employment_type=employment_type,
        is_current=is_current
    )
    
    return schemas.EmploymentListResponse(
        employments=employments,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=len(employments)
    )


@router.get("/{employment_id}", response_model=schemas.EmploymentWithCustomerResponse)
def get_employment(
    employment_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific employment by ID with customer information.
    
    - **employment_id**: The ID of the employment to retrieve
    """
    employment = crud.EmploymentCRUD.get_employment(db=db, employment_id=employment_id)
    if not employment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employment not found"
        )
    
    return employment


@router.get("/customer/{customer_id}", response_model=schemas.EmploymentResponse)
def get_employment_by_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve employment information for a specific customer.
    
    - **customer_id**: The ID of the customer
    """
    employment = crud.EmploymentCRUD.get_employment_by_customer(db=db, customer_id=customer_id)
    if not employment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employment information not found for this customer"
        )
    
    return employment


@router.put("/{employment_id}", response_model=schemas.EmploymentResponse)
def update_employment(
    employment_id: int,
    employment_update: schemas.EmploymentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update employment information.
    
    - **employment_id**: The ID of the employment to update
    - **employment_update**: The fields to update (all fields are optional)
    """
    return crud.EmploymentCRUD.update_employment(
        db=db, 
        employment_id=employment_id, 
        employment_data=employment_update
    )


@router.delete("/{employment_id}", response_model=schemas.MessageResponse)
def delete_employment(
    employment_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete employment information.
    
    - **employment_id**: The ID of the employment to delete
    """
    crud.EmploymentCRUD.delete_employment(db=db, employment_id=employment_id)
    return schemas.MessageResponse(
        message=f"Employment with ID {employment_id} has been deleted"
    ) 