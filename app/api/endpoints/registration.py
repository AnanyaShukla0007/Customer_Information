from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.CustomerWithEmploymentResponse, status_code=status.HTTP_201_CREATED)
def register_customer_with_employment(
    registration: schemas.CustomerRegistration,
    db: Session = Depends(get_db)
):
    """
    Register a new customer with their employment information in a single request.
    
    This endpoint creates both customer and employment records atomically.
    If either creation fails, the entire transaction is rolled back.
    
    **Customer Information:**
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
    
    **Employment Information:**
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
    try:
        customer, employment = crud.CustomerRegistrationCRUD.create_customer_with_employment(
            db=db, 
            registration_data=registration
        )
        
        return schemas.CustomerWithEmploymentResponse(
            **customer.__dict__,
            employment=employment
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as they already have proper status codes
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        ) 