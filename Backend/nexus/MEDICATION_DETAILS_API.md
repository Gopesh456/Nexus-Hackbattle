# Medication Details API Documentation

This document describes the two endpoints for storing and retrieving medication details information.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Endpoints

### 1. Store Medication Details
**POST** `/medication-details/store/`

Stores medication details for the authenticated user.

#### Request Format
```json
{
    "token": "your_jwt_token_here",
    "Medicine_name": "Metformin",
    "Frequency": "Twice daily",
    "Medical_Condition": "Type 2 Diabetes",
    "No_of_pills": "1 tablet",
    "next_order_data": "2025-10-15",
    "meds_reminder": "Take with meals to reduce stomach upset"
}
```

#### Field Descriptions
- **Medicine_name**: Name of the medication (String)
- **Frequency**: How often to take the medication (String)
- **Medical_Condition**: Condition for which the medication is prescribed (String)
- **No_of_pills**: Dosage information (String)
- **next_order_data**: Next order date in YYYY-MM-DD format (String)
- **meds_reminder**: Reminder notes or special instructions (String)

#### Success Response (200 OK)
```json
{
    "message": "Medication details stored successfully"
}
```

#### Error Responses
- **401 Unauthorized**: Invalid or missing token
- **404 Not Found**: User not found
- **400 Bad Request**: Invalid data format

---

### 2. Get Medication Details
**POST** `/medication-details/get/`

Retrieves the stored medication details for the authenticated user.

#### Request Format
```json
{
    "token": "your_jwt_token_here"
}
```

#### Success Response (200 OK)
```json
{
    "medicine_name": "Metformin",
    "frequency": "Twice daily",
    "medical_condition": "Type 2 Diabetes",
    "no_of_pills": "1 tablet",
    "next_order_date": "2025-10-15",
    "meds_reminder": "Take with meals to reduce stomach upset"
}
```

#### Error Responses
- **401 Unauthorized**: Invalid or missing token
- **404 Not Found**: User not found or no medication details found
- **400 Bad Request**: Invalid request format

---

## Field Mapping

The API automatically maps user-friendly input field names to database field names:

| Input Field Name | Database Field Name |
|------------------|-------------------|
| Medicine_name | medicine_name |
| Frequency | frequency |
| Medical_Condition | medical_condition |
| No_of_pills | no_of_pills |
| next_order_data | next_order_date |
| meds_reminder | meds_reminder |

## Usage Examples

### 1. Complete Workflow Example

**Step 1: Register and Login to get JWT token**
```bash
# Register
curl -X POST http://127.0.0.1:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass123"}'

# Login
curl -X POST http://127.0.0.1:8000/api/login/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass123"}'
```

**Step 2: Store medication details**
```bash
curl -X POST http://127.0.0.1:8000/api/medication-details/store/ \
-H "Content-Type: application/json" \
-d '{
  "token": "your_jwt_token_here",
  "Medicine_name": "Metformin",
  "Frequency": "Twice daily",
  "Medical_Condition": "Type 2 Diabetes",
  "No_of_pills": "1 tablet",
  "next_order_data": "2025-10-15",
  "meds_reminder": "Take with meals to reduce stomach upset"
}'
```

**Step 3: Retrieve medication details**
```bash
curl -X POST http://127.0.0.1:8000/api/medication-details/get/ \
-H "Content-Type: application/json" \
-d '{"token": "your_jwt_token_here"}'
```

### 2. Multiple Medication Example
```bash
# Store first medication
curl -X POST http://127.0.0.1:8000/medication-details/store/ \
-H "Content-Type: application/json" \
-d '{
  "token": "your_jwt_token_here",
  "Medicine_name": "Lisinopril",
  "Frequency": "Once daily",
  "Medical_Condition": "High Blood Pressure",
  "No_of_pills": "1 tablet (10mg)",
  "next_order_data": "2025-11-20",
  "meds_reminder": "Take in the morning, avoid potassium supplements"
}'

# Update with additional medication info (will overwrite previous)
curl -X POST http://127.0.0.1:8000/medication-details/store/ \
-H "Content-Type: application/json" \
-d '{
  "token": "your_jwt_token_here",
  "Medicine_name": "Atorvastatin",
  "Frequency": "Once daily at bedtime",
  "Medical_Condition": "High Cholesterol",
  "No_of_pills": "1 tablet (20mg)",
  "next_order_data": "2025-12-01",
  "meds_reminder": "Take with or without food, avoid grapefruit juice"
}'
```

### 3. Date Format Examples
```json
{
  "token": "your_jwt_token_here",
  "Medicine_name": "Aspirin",
  "Frequency": "Daily",
  "Medical_Condition": "Heart Disease Prevention", 
  "No_of_pills": "1 tablet (81mg)",
  "next_order_data": "2025-09-30",
  "meds_reminder": "Take with food to prevent stomach irritation"
}
```

## Important Notes

### Data Storage
- All medication fields are stored as strings to preserve formatting and units
- If a user already has medication details, the store endpoint will update the existing record
- Each user can have one medication details record (OneToOneField relationship)

### Date Format
- `next_order_data` field accepts dates in **YYYY-MM-DD** format only
- Examples: "2025-09-30", "2025-12-25", "2026-01-15"
- Invalid formats will cause validation errors

### Authentication
- All endpoints require JWT token authentication passed in the request body
- The API follows the same authentication pattern as other medical endpoints in the system

### Field Validation
- All fields are optional (blank=True) to allow partial updates
- Medicine_name: Maximum 255 characters
- Frequency: Maximum 100 characters  
- Medical_Condition: Maximum 255 characters
- No_of_pills: Maximum 50 characters
- meds_reminder: Maximum 255 characters

### Integration with Medical System
- The medication details endpoint follows the same structure as blood-test, metabolic-panel, and liver-function-test endpoints
- Consistent error handling and response formats across all medical data endpoints
- Seamless integration with the existing medical data management system

## Error Handling Examples

### Invalid Token
```json
{
  "error": "Invalid token provided"
}
```

### Missing Token
```json
{
  "error": "Token is required"
}
```

### No Data Found
```json
{
  "error": "No medication details found for this user"
}
```

### Invalid Date Format
```json
{
  "next_order_date": ["Enter a valid date."]
}
```