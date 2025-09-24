# Basic Info API Documentation

## Authentication
All endpoints require JWT token authentication. Include the token in the request body:
```json
{
    "token": "your_jwt_token",
    // ... other fields
}
```

## Endpoints

### 1. Submit Basic Info (Receive)
Submit or update user's basic information.

**Endpoint**: `/api/basic-info/receive/`

**Method**: `POST`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
    "token": "your_jwt_token",
    "full_name": "John Doe",
    "date_of_birth": "1995-05-15",
    "gender": "male",
    "location": "New York, USA",
    "email": "john.doe@example.com",
    "phone": "+1234567890"
}
```

**Field Requirements**:
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| full_name | string | User's full name | Required |
| date_of_birth | string | Birth date in YYYY-MM-DD format | Required, must be valid date |
| gender | string | User's gender | Must be one of: "male", "female", "other", "prefer_not_to_say" |
| location | string | User's location | Required |
| email | string | User's email address | Required, must be valid email format |
| phone | string | Phone number with country code | Must start with '+' and contain 9-15 digits |

**Success Response**:
- Status Code: 200 OK
```json
{
    "message": "Basic information saved successfully",
    "data": {
        "id": 1,
        "full_name": "John Doe",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "location": "New York, USA",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "age": 30
    }
}
```

**Error Responses**:

1. Invalid Data (400 Bad Request):
```json
{
    "error": "Invalid data",
    "details": {
        "field_name": ["Error message"]
    }
}
```

2. Authentication Error (401 Unauthorized):
```json
{
    "detail": "Authentication credentials were not provided"
}
```

### 2. Get Basic Info (Send)
Retrieve user's basic information.

**Endpoint**: `/api/basic-info/send/`

**Method**: `POST`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
    "token": "your_jwt_token"
}

**Success Response**:
- Status Code: 200 OK
```json
{
    "data": {
        "id": 1,
        "full_name": "John Doe",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "location": "New York, USA",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "age": 30
    }
}
```

**Error Responses**:

1. Data Not Found (404 Not Found):
```json
{
    "error": "Basic information not found for this user"
}
```

2. Authentication Error (401 Unauthorized):
```json
{
    "detail": "Authentication credentials were not provided"
}
```

## Code Examples

### Using JavaScript/Fetch

1. Submit Basic Info:
```javascript
const submitBasicInfo = async (token, userData) => {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/basic-info/receive/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: token,
                ...userData
            })
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to submit basic info');
        }
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
```

2. Get Basic Info:
```javascript
const getBasicInfo = async (token) => {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/basic-info/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: token
            })
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to get basic info');
        }
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
```

### Using Axios

1. Submit Basic Info:
```javascript
const submitBasicInfo = async (token, userData) => {
    try {
        const response = await axios.post(
            'http://127.0.0.1:8000/api/basic-info/receive/',
            userData,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
        throw error;
    }
};
```

2. Get Basic Info:
```javascript
const getBasicInfo = async (token) => {
    try {
        const response = await axios.post(
            'http://127.0.0.1:8000/api/basic-info/send/',
            {},
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
        throw error;
    }
};
```

## Usage Example

```javascript
// First get token from login
const token = 'your_jwt_token';

// Example: Submit basic info
const userData = {
    full_name: "John Doe",
    date_of_birth: "1995-05-15",
    gender: "male",
    location: "New York, USA",
    email: "john.doe@example.com",
    phone: "+1234567890"
};

// Submit basic info
try {
    const submitResult = await submitBasicInfo(token, userData);
    console.log('Basic info submitted:', submitResult);
    
    // Get basic info
    const basicInfo = await getBasicInfo(token);
    console.log('Basic info retrieved:', basicInfo);
} catch (error) {
    console.error('Error:', error);
}
```