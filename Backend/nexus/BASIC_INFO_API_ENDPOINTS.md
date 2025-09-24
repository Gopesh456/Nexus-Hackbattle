# Basic_Info API Endpoints Summary

## Overview
The Basic_Info model provides complete CRUD operations through RESTful API endpoints for managing user basic information.

## Data Format
All endpoints accept and return JSON data in this exact format:
```json
{
    "full_name": "string",
    "date_of_birth": "yyyy-mm-dd",
    "gender": "string",
    "location": "string", 
    "email": "string",
    "phone": "string"
}
```

## API Endpoints

### Base URL
```
http://127.0.0.1:8000/api
```

### 1. CREATE - Add New User Info
- **Endpoint**: `POST /basic-info/`
- **Purpose**: Create a new basic information record
- **Request Body**: JSON with all required fields
- **Response**: 201 Created with created record data
- **Example**:
  ```bash
  curl -X POST http://127.0.0.1:8000/api/basic-info/ \
    -H "Content-Type: application/json" \
    -d '{
      "full_name": "John Smith",
      "date_of_birth": "1995-03-15",
      "gender": "male",
      "location": "New York, USA",
      "email": "john@example.com",
      "phone": "+1234567890"
    }'
  ```

### 2. READ - Get All Records  
- **Endpoint**: `GET /basic-info/all/`
- **Purpose**: Retrieve all basic information records
- **Parameters**: None
- **Response**: 200 OK with list of all records
- **Example**:
  ```bash
  curl -X GET http://127.0.0.1:8000/api/basic-info/all/
  ```

### 3. READ - Get Single Record
- **Endpoint**: `GET /basic-info/{id}/`
- **Purpose**: Retrieve a specific record by ID
- **Parameters**: `id` - Record ID in URL path
- **Response**: 200 OK with single record data
- **Example**:
  ```bash
  curl -X GET http://127.0.0.1:8000/api/basic-info/1/
  ```

### 4. UPDATE - Modify Existing Record
- **Endpoint**: `PUT /basic-info/{id}/update/` or `PATCH /basic-info/{id}/update/`
- **Purpose**: Update an existing record
- **Parameters**: `id` - Record ID in URL path
- **Methods**:
  - `PUT`: Full update (all fields required)
  - `PATCH`: Partial update (only changed fields required)
- **Response**: 200 OK with updated record data
- **Example**:
  ```bash
  curl -X PATCH http://127.0.0.1:8000/api/basic-info/1/update/ \
    -H "Content-Type: application/json" \
    -d '{
      "location": "Los Angeles, USA",
      "phone": "+1987654321"
    }'
  ```

### 5. DELETE - Remove Record
- **Endpoint**: `DELETE /basic-info/{id}/delete/`
- **Purpose**: Delete a specific record
- **Parameters**: `id` - Record ID in URL path
- **Response**: 200 OK with confirmation of deleted record
- **Example**:
  ```bash
  curl -X DELETE http://127.0.0.1:8000/api/basic-info/1/delete/
  ```

### 6. SEARCH - Filter Records
- **Endpoint**: `GET /basic-info/search/`
- **Purpose**: Search records using query parameters
- **Query Parameters**:
  - `full_name`: Partial name search (case-insensitive)
  - `email`: Exact email match
  - `location`: Partial location search (case-insensitive)
  - `gender`: Exact gender match
- **Response**: 200 OK with filtered records
- **Examples**:
  ```bash
  # Search by gender
  curl -X GET "http://127.0.0.1:8000/api/basic-info/search/?gender=female"
  
  # Search by location
  curl -X GET "http://127.0.0.1:8000/api/basic-info/search/?location=USA"
  
  # Search by name
  curl -X GET "http://127.0.0.1:8000/api/basic-info/search/?full_name=John"
  
  # Multiple filters
  curl -X GET "http://127.0.0.1:8000/api/basic-info/search/?gender=male&location=New%20York"
  ```

## Response Format

### Success Responses

#### Create/Update Success (201/200)
```json
{
    "message": "Basic information created successfully",
    "data": {
        "id": 1,
        "full_name": "John Smith",
        "date_of_birth": "1995-03-15",
        "gender": "male",
        "location": "New York, USA",
        "email": "john@example.com",
        "phone": "+1234567890",
        "age": 30,
        "created_at": "2025-09-24T15:30:00.000Z",
        "updated_at": "2025-09-24T15:30:00.000Z"
    }
}
```

#### List/Search Success (200)
```json
{
    "count": 2,
    "data": [
        {
            "id": 1,
            "full_name": "John Smith",
            "date_of_birth": "1995-03-15",
            "gender": "male",
            "location": "New York, USA",
            "email": "john@example.com",
            "phone": "+1234567890",
            "age": 30,
            "created_at": "2025-09-24T15:30:00.000Z",
            "updated_at": "2025-09-24T15:30:00.000Z"
        }
    ]
}
```

#### Delete Success (200)
```json
{
    "message": "Basic information deleted successfully",
    "deleted_record": {
        "id": 1,
        "full_name": "John Smith",
        "email": "john@example.com"
    }
}
```

### Error Responses

#### Validation Error (400)
```json
{
    "error": "Invalid data",
    "details": {
        "email": ["Enter a valid email address."],
        "phone": ["Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."],
        "date_of_birth": ["Date of birth cannot be in the future."]
    }
}
```

#### Not Found (404)
```json
{
    "detail": "Not found."
}
```

## Field Validation Rules

| Field | Rules |
|-------|-------|
| `full_name` | Required, max 255 characters |
| `date_of_birth` | Required, YYYY-MM-DD format, not in future, age ≤ 120 |
| `gender` | Required, choices: `male`, `female`, `other`, `prefer_not_to_say` |
| `location` | Required, max 255 characters |
| `email` | Required, valid email format, unique |
| `phone` | Required, format: `+1234567890`, 9-15 digits |

## Quick Test Commands

### Test All Endpoints
```bash
# 1. Create a record
curl -X POST http://127.0.0.1:8000/api/basic-info/ \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Test User", "date_of_birth": "1990-01-01", "gender": "male", "location": "Test City", "email": "test@example.com", "phone": "+1234567890"}'

# 2. Get all records
curl -X GET http://127.0.0.1:8000/api/basic-info/all/

# 3. Get specific record (replace 1 with actual ID)
curl -X GET http://127.0.0.1:8000/api/basic-info/1/

# 4. Update record (replace 1 with actual ID)
curl -X PATCH http://127.0.0.1:8000/api/basic-info/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"location": "Updated City"}'

# 5. Search records
curl -X GET "http://127.0.0.1:8000/api/basic-info/search/?gender=male"

# 6. Delete record (replace 1 with actual ID)
curl -X DELETE http://127.0.0.1:8000/api/basic-info/1/delete/
```

## Python Example
```python
import requests
import json

base_url = "http://127.0.0.1:8000/api"

# Create a new record
data = {
    "full_name": "Alice Johnson",
    "date_of_birth": "1992-06-15",
    "gender": "female",
    "location": "Seattle, WA",
    "email": "alice@example.com",
    "phone": "+1206555000"
}

response = requests.post(f"{base_url}/basic-info/", json=data)
print("Created:", response.json())

# Get all records
response = requests.get(f"{base_url}/basic-info/all/")
print("All records:", response.json())

# Search by gender
response = requests.get(f"{base_url}/basic-info/search/", params={"gender": "female"})
print("Female users:", response.json())
```

## Testing

To run comprehensive tests:
```bash
# Install requests library
pip install requests

# Start Django server
python manage.py runserver

# Run API tests (in another terminal)
python test_basic_info.py

# Or run model verification
python verify_basic_info.py
```

This API provides complete CRUD functionality for managing user basic information with proper validation, error handling, and search capabilities.