# Appointment Management API Documentation

## Overview
The Appointment Management API allows users to store and retrieve their medical appointments. Users can track appointments with various doctors, including details about location, specialization, type, and purpose.

## Base URL
```
http://127.0.0.1:8000/api
```

## Authentication
All endpoints require JWT authentication. Include the JWT token in the request body as shown in the examples below.

---

## Endpoints

### 1. Store Appointment
Store a new appointment for the authenticated user.

**URL:** `/appointments/store/`  
**Method:** `POST`  
**Authentication:** Required (JWT Token)

#### Request Body
```json
{
  "token": "your_jwt_token_here",
  "appointment_date": "2025-09-30T14:30:00Z",
  "location": "City Medical Center, 123 Healthcare Blvd, New York, NY 10001",
  "doctor_name": "Dr. Sarah Johnson",
  "doctor_specialization": "Cardiology",
  "appointment_type": "consultant",
  "reason": "Follow-up for heart murmur detected during routine checkup"
}
```

#### Field Descriptions
| Field | Type | Required | Description | Example Values |
|-------|------|----------|-------------|----------------|
| `token` | string | Yes | JWT authentication token | "eyJ0eXAiOiJKV1QiLCJ..." |
| `appointment_date` | string | Yes | Date and time in ISO 8601 format | "2025-09-30T14:30:00Z" |
| `location` | string | Yes | Full address or location name | "City Medical Center, NY" |
| `doctor_name` | string | Yes | Full name of the doctor | "Dr. Sarah Johnson" |
| `doctor_specialization` | string | Yes | Doctor's medical specialization | "Cardiology", "Dermatology" |
| `appointment_type` | string | Yes | Type of appointment | "general", "consultant" |
| `reason` | string | Yes | Purpose/reason for the appointment | "Routine checkup", "Follow-up" |

#### Appointment Types
- **`general`**: Regular checkups, basic consultations, preventive care
- **`consultant`**: Specialist consultations, follow-ups, specialized treatments

#### Success Response (201 Created)
```json
{
  "message": "Appointment stored successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "appointment_date": "2025-09-30T14:30:00Z",
    "location": "City Medical Center, 123 Healthcare Blvd, New York, NY 10001",
    "doctor_name": "Dr. Sarah Johnson",
    "doctor_specialization": "Cardiology",
    "appointment_type": "consultant",
    "reason": "Follow-up for heart murmur detected during routine checkup",
    "created_at": "2025-09-25T10:15:30Z",
    "updated_at": "2025-09-25T10:15:30Z"
  }
}
```

#### Error Responses
**401 Unauthorized - Missing Token**
```json
{
  "error": "Token is required"
}
```

**401 Unauthorized - Invalid Token**
```json
{
  "error": "Invalid token provided"
}
```

**400 Bad Request - Invalid Data**
```json
{
  "error": "Invalid data provided",
  "details": {
    "appointment_date": ["This field is required."],
    "appointment_type": ["\"invalid_type\" is not a valid choice."]
  }
}
```

---

### 2. Get Appointments  
Retrieve all appointments for the authenticated user.

**URL:** `/appointments/get/`  
**Method:** `POST`  
**Authentication:** Required (JWT Token)

#### Request Body
```json
{
  "token": "your_jwt_token_here"
}
```

#### Success Response (200 OK)
```json
{
  "user": "john_doe",
  "count": 3,
  "appointments": [
    {
      "id": 3,
      "username": "john_doe",
      "appointment_date": "2025-10-15T09:00:00Z",
      "location": "Downtown Clinic, 456 Main St, NY",
      "doctor_name": "Dr. Michael Brown",
      "doctor_specialization": "Dermatology",
      "appointment_type": "general",
      "reason": "Annual skin check",
      "created_at": "2025-09-25T10:20:00Z",
      "updated_at": "2025-09-25T10:20:00Z"
    },
    {
      "id": 2,
      "username": "john_doe", 
      "appointment_date": "2025-10-01T16:00:00Z",
      "location": "Orthopedic Specialists, 789 Health Ave, NY",
      "doctor_name": "Dr. Lisa Chen",
      "doctor_specialization": "Orthopedics",
      "appointment_type": "consultant",
      "reason": "Knee pain assessment",
      "created_at": "2025-09-25T10:18:00Z",
      "updated_at": "2025-09-25T10:18:00Z"
    },
    {
      "id": 1,
      "username": "john_doe",
      "appointment_date": "2025-09-30T14:30:00Z", 
      "location": "City Medical Center, 123 Healthcare Blvd, NY",
      "doctor_name": "Dr. Sarah Johnson",
      "doctor_specialization": "Cardiology",
      "appointment_type": "consultant",
      "reason": "Follow-up for heart murmur",
      "created_at": "2025-09-25T10:15:30Z",
      "updated_at": "2025-09-25T10:15:30Z"
    }
  ]
}
```

#### Error Responses
**401 Unauthorized - Missing Token**
```json
{
  "error": "Token is required"
}
```

**401 Unauthorized - Invalid Token**
```json
{
  "error": "Invalid token provided"
}
```

**500 Internal Server Error**
```json
{
  "error": "Failed to retrieve appointments",
  "details": "Error message details"
}
```

---

## Usage Examples

### JavaScript/Frontend Integration
```javascript
class AppointmentAPI {
  constructor(baseURL = 'http://127.0.0.1:8000/api') {
    this.baseURL = baseURL;
  }

  async storeAppointment(token, appointmentData) {
    const response = await fetch(`${this.baseURL}/appointments/store/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        token: token,
        ...appointmentData
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to store appointment');
    }

    return await response.json();
  }

  async getAppointments(token) {
    const response = await fetch(`${this.baseURL}/appointments/get/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to retrieve appointments');
    }

    return await response.json();
  }
}

// Usage
const appointmentAPI = new AppointmentAPI();

// Store appointment
try {
  const result = await appointmentAPI.storeAppointment('your_jwt_token', {
    appointment_date: '2025-09-30T14:30:00Z',
    location: 'City Medical Center, NY',
    doctor_name: 'Dr. Sarah Johnson',
    doctor_specialization: 'Cardiology',
    appointment_type: 'consultant',
    reason: 'Follow-up consultation'
  });
  console.log('Appointment stored:', result);
} catch (error) {
  console.error('Error:', error.message);
}

// Get appointments
try {
  const appointments = await appointmentAPI.getAppointments('your_jwt_token');
  console.log('User appointments:', appointments);
} catch (error) {
  console.error('Error:', error.message);
}
```

### Python/Backend Integration
```python
import requests
import json
from datetime import datetime

class AppointmentClient:
    def __init__(self, base_url='http://127.0.0.1:8000/api'):
        self.base_url = base_url
    
    def store_appointment(self, token, appointment_data):
        """Store a new appointment"""
        url = f"{self.base_url}/appointments/store/"
        data = {'token': token, **appointment_data}
        
        response = requests.post(url, json=data)
        return response.json()
    
    def get_appointments(self, token):
        """Get all user appointments"""
        url = f"{self.base_url}/appointments/get/"
        data = {'token': token}
        
        response = requests.post(url, json=data)
        return response.json()

# Usage
client = AppointmentClient()

# Store appointment
appointment_data = {
    'appointment_date': '2025-09-30T14:30:00Z',
    'location': 'City Medical Center, NY',
    'doctor_name': 'Dr. Sarah Johnson',
    'doctor_specialization': 'Cardiology',
    'appointment_type': 'consultant',
    'reason': 'Follow-up consultation'
}

result = client.store_appointment('your_jwt_token', appointment_data)
print("Stored appointment:", result)

# Get appointments
appointments = client.get_appointments('your_jwt_token')
print("User appointments:", appointments)
```

---

## Common Medical Specializations
- **Cardiology** - Heart and cardiovascular system
- **Dermatology** - Skin, hair, and nails
- **Neurology** - Brain and nervous system
- **Orthopedics** - Bones, joints, and muscles
- **Pediatrics** - Children's health
- **Psychiatry** - Mental health
- **Radiology** - Medical imaging
- **Oncology** - Cancer treatment
- **Internal Medicine** - Adult internal organs
- **Family Medicine** - General family healthcare
- **Endocrinology** - Hormones and metabolism
- **Gastroenterology** - Digestive system
- **Pulmonology** - Lungs and respiratory system
- **Rheumatology** - Autoimmune and joint diseases

---

## Date Format Guidelines
Always use ISO 8601 format for appointment dates:
- **Format**: `YYYY-MM-DDTHH:MM:SSZ`
- **Example**: `2025-09-30T14:30:00Z`
- **Time Zone**: Use UTC (Z suffix) or specify timezone offset

---

## Best Practices
1. **Validation**: Always validate appointment dates to ensure they are in the future
2. **Time Zones**: Store appointments in UTC and convert to local time in frontend
3. **Reminders**: Consider implementing appointment reminders based on the stored data
4. **Updates**: The current API stores appointments; consider adding update/delete endpoints
5. **Pagination**: For users with many appointments, implement pagination in the get endpoint