from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.api import api_router
from app.config import settings
from app.database import engine
from app import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    description="""
    ## Customer Registration System API
    
    A comprehensive RESTful API for managing customer registrations with personal and employment information.
    
    ### Features:
    - **Customer Management**: Create, read, update, and delete customer information
    - **Employment Management**: Manage employment details for customers
    - **Combined Registration**: Register customers with employment information in a single request
    - **Search and Filtering**: Advanced search and filtering capabilities
    - **Pagination**: Built-in pagination for large datasets
    - **Validation**: Comprehensive input validation and error handling
    
    ### API Endpoints:
    
    #### Customers (`/api/v1/customers`)
    - `POST /` - Create a new customer
    - `GET /` - List customers with pagination and filtering
    - `GET /{customer_id}` - Get customer by ID with employment info
    - `PUT /{customer_id}` - Update customer information
    - `DELETE /{customer_id}` - Soft delete customer
    - `DELETE /{customer_id}/hard` - Permanently delete customer
    - `GET /email/{email}` - Get customer by email
    
    #### Employments (`/api/v1/employments`)
    - `POST /` - Create employment for a customer
    - `GET /` - List employments with pagination and filtering
    - `GET /{employment_id}` - Get employment by ID with customer info
    - `GET /customer/{customer_id}` - Get employment by customer ID
    - `PUT /{employment_id}` - Update employment information
    - `DELETE /{employment_id}` - Delete employment
    
    #### Registration (`/api/v1/registration`)
    - `POST /` - Register customer with employment in single request
    
    ### Data Models:
    
    **Customer Fields:**
    - `first_name` (required): Customer's first name
    - `last_name` (required): Customer's last name
    - `email` (required, unique): Customer's email address
    - `phone` (required): Customer's phone number (min 10 digits)
    - `date_of_birth` (required): Customer's date of birth
    - `address` (required): Customer's address
    - `city` (required): Customer's city
    - `state` (required): Customer's state/province
    - `postal_code` (required): Customer's postal code
    - `country` (required): Customer's country
    
    **Employment Fields:**
    - `company_name` (required): Name of the company
    - `job_title` (required): Job title/position
    - `department` (optional): Department
    - `employment_type` (required): Type of employment (Full-time, Part-time, Contract, etc.)
    - `start_date` (required): Employment start date
    - `end_date` (optional): Employment end date
    - `salary` (optional): Salary information
    - `work_address` (optional): Work address
    - `work_city` (optional): Work city
    - `work_state` (optional): Work state/province
    - `work_postal_code` (optional): Work postal code
    - `work_country` (optional): Work country
    - `is_current_employment` (optional): Whether this is current employment
    
    ### Validation Rules:
    - Email addresses must be valid and unique
    - Phone numbers must contain at least 10 digits
    - Date of birth cannot be in the future or before 1900
    - Employment start date cannot be in the future
    - Employment end date must be after start date (if provided)
    
    ### Error Handling:
    The API returns appropriate HTTP status codes and detailed error messages:
    - `400 Bad Request`: Validation errors or business rule violations
    - `404 Not Found`: Resource not found
    - `500 Internal Server Error`: Unexpected server errors
    
    ### Authentication:
    Currently, this API does not require authentication. In production, implement proper authentication and authorization.
    """,
    version="1.0.0",
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_v1_str)

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "success": False
        }
    )

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint providing basic API information.
    """
    return {
        "message": "Welcome to Customer Registration System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": settings.api_v1_str
    }

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint to verify API status.
    """
    return {
        "status": "healthy",
        "message": "Customer Registration System API is running",
        "success": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 