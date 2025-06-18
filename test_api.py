#!/usr/bin/env python3
"""
Simple test script to demonstrate the Customer Registration API functionality.
Run this after starting the API server.
"""

import requests
import json
from datetime import date

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health_check():
    """Test health check endpoint"""
    response = requests.get("http://localhost:8000/health")
    print_response(response, "Health Check")

def test_register_customer_with_employment():
    """Test combined customer and employment registration"""
    data = {
        "customer": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "date_of_birth": "1990-01-15",
            "address": "123 Main Street",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "USA"
        },
        "employment": {
            "company_name": "Tech Corp",
            "job_title": "Software Engineer",
            "department": "Engineering",
            "employment_type": "Full-time",
            "start_date": "2020-03-01",
            "salary": "$80,000",
            "work_address": "456 Business Ave",
            "work_city": "New York",
            "work_state": "NY",
            "work_postal_code": "10002",
            "work_country": "USA",
            "is_current_employment": True
        }
    }
    
    response = requests.post(f"{BASE_URL}/registration/", json=data)
    print_response(response, "Register Customer with Employment")
    return response.json()

def test_create_customer_only():
    """Test creating a customer without employment"""
    data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "+1-555-987-6543",
        "date_of_birth": "1985-06-20",
        "address": "789 Oak Drive",
        "city": "Los Angeles",
        "state": "CA",
        "postal_code": "90210",
        "country": "USA"
    }
    
    response = requests.post(f"{BASE_URL}/customers/", json=data)
    print_response(response, "Create Customer Only")
    return response.json()

def test_add_employment_to_customer(customer_id):
    """Test adding employment to an existing customer"""
    data = {
        "company_name": "Design Studio",
        "job_title": "UI/UX Designer",
        "department": "Design",
        "employment_type": "Full-time",
        "start_date": "2019-01-15",
        "salary": "$75,000",
        "work_address": "321 Creative Blvd",
        "work_city": "Los Angeles",
        "work_state": "CA",
        "work_postal_code": "90211",
        "work_country": "USA",
        "is_current_employment": True
    }
    
    response = requests.post(f"{BASE_URL}/employments/?customer_id={customer_id}", json=data)
    print_response(response, f"Add Employment to Customer {customer_id}")

def test_get_customers():
    """Test getting list of customers"""
    response = requests.get(f"{BASE_URL}/customers/")
    print_response(response, "Get All Customers")

def test_search_customers():
    """Test searching customers"""
    response = requests.get(f"{BASE_URL}/customers/?search=john")
    print_response(response, "Search Customers (john)")

def test_get_customer_by_id(customer_id):
    """Test getting a specific customer"""
    response = requests.get(f"{BASE_URL}/customers/{customer_id}")
    print_response(response, f"Get Customer {customer_id}")

def test_get_customer_by_email(email):
    """Test getting a customer by email"""
    response = requests.get(f"{BASE_URL}/customers/email/{email}")
    print_response(response, f"Get Customer by Email: {email}")

def test_update_customer(customer_id):
    """Test updating a customer"""
    data = {
        "phone": "+1-555-999-8888",
        "city": "San Francisco"
    }
    
    response = requests.put(f"{BASE_URL}/customers/{customer_id}", json=data)
    print_response(response, f"Update Customer {customer_id}")

def test_get_employments():
    """Test getting list of employments"""
    response = requests.get(f"{BASE_URL}/employments/")
    print_response(response, "Get All Employments")

def test_search_employments():
    """Test searching employments"""
    response = requests.get(f"{BASE_URL}/employments/?search=tech")
    print_response(response, "Search Employments (tech)")

def main():
    """Run all tests"""
    print("Starting Customer Registration API Tests")
    print("Make sure the API server is running on http://localhost:8000")
    
    try:
        # Test health check
        test_health_check()
        
        # Test registration
        registration_result = test_register_customer_with_employment()
        customer_id_1 = registration_result.get('id')
        
        # Test creating customer only
        customer_result = test_create_customer_only()
        customer_id_2 = customer_result.get('id')
        
        # Test adding employment to existing customer
        if customer_id_2:
            test_add_employment_to_customer(customer_id_2)
        
        # Test getting customers
        test_get_customers()
        test_search_customers()
        
        # Test getting specific customer
        if customer_id_1:
            test_get_customer_by_id(customer_id_1)
            test_get_customer_by_email("john.doe@example.com")
            test_update_customer(customer_id_1)
        
        # Test employments
        test_get_employments()
        test_search_employments()
        
        print("\n" + "="*50)
        print("All tests completed!")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 