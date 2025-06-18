from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional
from datetime import date, datetime
from enum import Enum


class EmploymentType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    FREELANCE = "Freelance"
    INTERNSHIP = "Internship"
    TEMPORARY = "Temporary"


# Base schemas
class CustomerBase(BaseModel):
    first_name: constr(min_length=1, max_length=50, strip_whitespace=True)
    last_name: constr(min_length=1, max_length=50, strip_whitespace=True)
    email: EmailStr
    phone: constr(min_length=10, max_length=20, strip_whitespace=True)
    date_of_birth: date
    address: constr(min_length=5, max_length=500, strip_whitespace=True)
    city: constr(min_length=1, max_length=50, strip_whitespace=True)
    state: constr(min_length=1, max_length=50, strip_whitespace=True)
    postal_code: constr(min_length=3, max_length=10, strip_whitespace=True)
    country: constr(min_length=1, max_length=50, strip_whitespace=True)
    
    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v >= date.today():
            raise ValueError('Date of birth cannot be in the future')
        if v.year < 1900:
            raise ValueError('Date of birth cannot be before 1900')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        # Remove all non-digit characters for validation
        digits_only = ''.join(filter(str.isdigit, v))
        if len(digits_only) < 10:
            raise ValueError('Phone number must contain at least 10 digits')
        return v


class EmploymentBase(BaseModel):
    company_name: constr(min_length=1, max_length=100, strip_whitespace=True)
    job_title: constr(min_length=1, max_length=100, strip_whitespace=True)
    department: Optional[constr(max_length=100, strip_whitespace=True)] = None
    employment_type: EmploymentType
    start_date: date
    end_date: Optional[date] = None
    salary: Optional[constr(max_length=50, strip_whitespace=True)] = None
    work_address: Optional[constr(max_length=500, strip_whitespace=True)] = None
    work_city: Optional[constr(max_length=50, strip_whitespace=True)] = None
    work_state: Optional[constr(max_length=50, strip_whitespace=True)] = None
    work_postal_code: Optional[constr(max_length=10, strip_whitespace=True)] = None
    work_country: Optional[constr(max_length=50, strip_whitespace=True)] = None
    is_current_employment: bool = True
    
    @validator('start_date')
    def validate_start_date(cls, v):
        if v > date.today():
            raise ValueError('Start date cannot be in the future')
        return v
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v


# Create schemas
class CustomerCreate(CustomerBase):
    pass


class EmploymentCreate(EmploymentBase):
    pass


class CustomerRegistration(BaseModel):
    customer: CustomerCreate
    employment: EmploymentCreate


# Update schemas
class CustomerUpdate(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    last_name: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    email: Optional[EmailStr] = None
    phone: Optional[constr(min_length=10, max_length=20, strip_whitespace=True)] = None
    date_of_birth: Optional[date] = None
    address: Optional[constr(min_length=5, max_length=500, strip_whitespace=True)] = None
    city: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    state: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    postal_code: Optional[constr(min_length=3, max_length=10, strip_whitespace=True)] = None
    country: Optional[constr(min_length=1, max_length=50, strip_whitespace=True)] = None
    is_active: Optional[bool] = None


class EmploymentUpdate(BaseModel):
    company_name: Optional[constr(min_length=1, max_length=100, strip_whitespace=True)] = None
    job_title: Optional[constr(min_length=1, max_length=100, strip_whitespace=True)] = None
    department: Optional[constr(max_length=100, strip_whitespace=True)] = None
    employment_type: Optional[EmploymentType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    salary: Optional[constr(max_length=50, strip_whitespace=True)] = None
    work_address: Optional[constr(max_length=500, strip_whitespace=True)] = None
    work_city: Optional[constr(max_length=50, strip_whitespace=True)] = None
    work_state: Optional[constr(max_length=50, strip_whitespace=True)] = None
    work_postal_code: Optional[constr(max_length=10, strip_whitespace=True)] = None
    work_country: Optional[constr(max_length=50, strip_whitespace=True)] = None
    is_current_employment: Optional[bool] = None


# Response schemas
class CustomerResponse(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class EmploymentResponse(EmploymentBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CustomerWithEmploymentResponse(CustomerResponse):
    employment: Optional[EmploymentResponse] = None


class EmploymentWithCustomerResponse(EmploymentResponse):
    customer: CustomerResponse


# List response schemas
class CustomerListResponse(BaseModel):
    customers: list[CustomerResponse]
    total: int
    page: int
    size: int


class EmploymentListResponse(BaseModel):
    employments: list[EmploymentWithCustomerResponse]
    total: int
    page: int
    size: int


# Message responses
class MessageResponse(BaseModel):
    message: str
    success: bool = True 