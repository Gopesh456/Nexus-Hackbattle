# Nexus API Documentation (Single Token Authentication)

## Base URL
```
http://127.0.0.1:8000/api
```

## Authentication Endpoints

### Register User
Create a new user account.

- **URL**: `/register/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "username": "your_username",
    "password": "your_password",
    "email": "your.email@example.com"  // optional
}
```
- **Success Response**:
  - **Code**: 201 CREATED
  - **Content**:
```json
{
    "message": "User registered successfully",
    "user_id": 1,
    "tokens": {
        "refresh": "refresh_token_here",
        "access": "access_token_here"
    }
}
```
- **Error Response**:
  - **Code**: 400 BAD REQUEST
  - **Content**:
```json
{
    "username": ["This field is required"],
    "password": ["This field is required"]
}
```

### Login User
Login with existing credentials.

- **URL**: `/login/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "your_username",
        "email": "your.email@example.com"
    },
    "tokens": {
        "access": "access_token_here",
        "refresh": "refresh_token_here"
    }
}
```
- **Error Response**:
  - **Code**: 401 UNAUTHORIZED
  - **Content**:
```json
{
    "error": "Invalid credentials"
}
```

## Basic Info Endpoints

### Submit Basic Info
Submit or update user's basic information.

- **URL**: `/basic-info/receive/`
- **Method**: `POST`
- **Authentication**: Required
- **Headers**:
```
Authorization: Bearer your_access_token
```
- **Request Body**:
```json
{
    "full_name": "John Doe",
    "date_of_birth": "1995-05-15",
    "gender": "male",
    "location": "New York, USA",
    "email": "john@example.com",
    "phone": "+1234567890"
}
```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
    "message": "Basic information saved successfully",
    "data": {
        "id": 1,
        "full_name": "John Doe",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "location": "New York, USA",
        "email": "john@example.com",
        "phone": "+1234567890",
        "age": 30
    }
}
```
- **Error Response**:
  - **Code**: 400 BAD REQUEST
  - **Content**:
```json
{
    "error": "Error message here"
}
```

### Get Basic Info
Retrieve user's basic information.

- **URL**: `/basic-info/send/`
- **Method**: `GET`
- **Authentication**: Required
- **Headers**:
```
Authorization: Bearer your_access_token
```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
    "data": {
        "id": 1,
        "full_name": "John Doe",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "location": "New York, USA",
        "email": "john@example.com",
        "phone": "+1234567890",
        "age": 30
    }
}
```
- **Error Response**:
  - **Code**: 404 NOT FOUND
  - **Content**:
```json
{
    "error": "Basic information not found for this user"
}
```

### Update Basic Info
Update specific fields of user's basic information.

- **URL**: `/basic-info/{id}/update/`
- **Method**: `PUT` or `PATCH`
- **Authentication**: Required
- **Headers**:
```
Authorization: Bearer your_access_token
```
- **Request Body** (for PATCH, include only fields to update):
```json
{
    "full_name": "John Doe Updated",
    "location": "Los Angeles, USA"
}
```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
    "message": "Basic information updated successfully",
    "data": {
        "id": 1,
        "full_name": "John Doe Updated",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "location": "Los Angeles, USA",
        "email": "john@example.com",
        "phone": "+1234567890",
        "age": 30
    }
}
```

### Delete Basic Info
Delete user's basic information.

- **URL**: `/basic-info/{id}/delete/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Headers**:
```
Authorization: Bearer your_access_token
```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
    "message": "Basic information deleted successfully",
    "deleted_record": {
        "id": 1,
        "full_name": "John Doe",
        "email": "john@example.com"
    }
}
```

### Search Basic Info
Search through basic information records.

- **URL**: `/basic-info/search/`
- **Method**: `GET`
- **Authentication**: Required
- **Headers**:
```
Authorization: Bearer your_access_token
```
- **Query Parameters**:
  - `full_name`: Search by name (partial match)
  - `email`: Search by email (exact match)
  - `location`: Search by location (partial match)
  - `gender`: Search by gender (exact match)
- **Example**: `/api/basic-info/search/?full_name=John&location=New York`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
    "count": 1,
    "data": [{
        "id": 1,
        "full_name": "John Doe",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "location": "New York, USA",
        "email": "john@example.com",
        "phone": "+1234567890",
        "age": 30
    }],
    "filters_applied": {
        "full_name": "John",
        "location": "New York",
        "email": null,
        "gender": null
    }
}
```

## Data Validation

### Gender Choices
Valid gender values:
- `male`
- `female`
- `other`
- `prefer_not_to_say`

### Phone Number Format
Phone numbers must:
- Start with optional '+' followed by country code
- Contain 9-15 digits
- Example: `+1234567890`

### Date Format
Dates must be in ISO format: `YYYY-MM-DD`

## Error Handling

All endpoints may return these common errors:

- **401 Unauthorized**:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

- **400 Bad Request**:
```json
{
    "error": "Invalid data",
    "details": {
        "field_name": ["Error message"]
    }
}
```

- **404 Not Found**:
```json
{
    "error": "Resource not found"
}
```

## Token Management

### Token Refresh
Refresh an expired access token using refresh token.

- **URL**: `/token/refresh/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "refresh": "your_refresh_token"
}
```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
    "access": "new_access_token_here"
}
```