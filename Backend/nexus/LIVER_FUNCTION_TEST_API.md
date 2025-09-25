# Liver Function Test API Documentation

This document describes the two endpoints for storing and retrieving liver function test results.

## Base URL
```
http://127.0.0.1:8000/
```

## Endpoints

### 1. Store Liver Function Test
**POST** `/liver-function-test/store/`

Stores liver function test results for the authenticated user.

#### Request Format
```json
{
    "token": "your_jwt_token_here",
    "Total Protein": "7.0 g/dL",
    "Albumin": "4.5 g/dL",
    "Globulin": "2.5 g/dL",
    "A/G Ratio": "1.8",
    "Total Bilirubin": "0.8 mg/dL",
    "Direct Bilirubin": "0.2 mg/dL",
    "Indirect Bilirubin": "0.6 mg/dL",
    "AST (SGOT)": "25 U/L",
    "ALT (SGPT)": "30 U/L",
    "Alkaline Phosphatase": "90 U/L",
    "GGT": "20 U/L"
}
```

#### Optional Fields (can be included in request)
```json
{
    "test_date": "2025-09-25",
    "lab_name": "City Medical Lab",
    "doctor_name": "Dr. Smith"
}
```

#### Success Response (200 OK)
```json
{
    "message": "Liver function test stored successfully"
}
```

#### Error Responses
- **401 Unauthorized**: Invalid or missing token
- **404 Not Found**: User not found
- **400 Bad Request**: Invalid data format

---

### 2. Get Liver Function Test
**POST** `/liver-function-test/get/`

Retrieves the stored liver function test results for the authenticated user.

#### Request Format
```json
{
    "token": "your_jwt_token_here"
}
```

#### Success Response (200 OK)
```json
{
    "total_protein": "7.0 g/dL",
    "albumin": "4.5 g/dL",
    "globulin": "2.5 g/dL",
    "ag_ratio": "1.8",
    "total_bilirubin": "0.8 mg/dL",
    "direct_bilirubin": "0.2 mg/dL",
    "indirect_bilirubin": "0.6 mg/dL",
    "ast_sgot": "25 U/L",
    "alt_sgpt": "30 U/L",
    "alkaline_phosphatase": "90 U/L",
    "ggt": "20 U/L",
    "test_date": "2025-09-25",
    "lab_name": "City Medical Lab",
    "doctor_name": "Dr. Smith"
}
```

#### Error Responses
- **401 Unauthorized**: Invalid or missing token
- **404 Not Found**: User not found or no liver function test data found
- **400 Bad Request**: Invalid request format

---

## Field Mapping

The API automatically maps user-friendly input field names to database field names:

| Input Field Name | Database Field Name |
|------------------|-------------------|
| Total Protein | total_protein |
| Albumin | albumin |
| Globulin | globulin |
| A/G Ratio | ag_ratio |
| Total Bilirubin | total_bilirubin |
| Direct Bilirubin | direct_bilirubin |
| Indirect Bilirubin | indirect_bilirubin |
| AST (SGOT) | ast_sgot |
| ALT (SGPT) | alt_sgpt |
| Alkaline Phosphatase | alkaline_phosphatase |
| GGT | ggt |

## Usage Example

1. **First, register and login to get a JWT token:**
   ```bash
   # Register
   curl -X POST http://127.0.0.1:8000/register/ \
   -H "Content-Type: application/json" \
   -d '{"username": "testuser", "password": "testpass123"}'
   
   # Login
   curl -X POST http://127.0.0.1:8000/login/ \
   -H "Content-Type: application/json" \
   -d '{"username": "testuser", "password": "testpass123"}'
   ```

2. **Store liver function test results:**
   ```bash
   curl -X POST http://127.0.0.1:8000/liver-function-test/store/ \
   -H "Content-Type: application/json" \
   -d '{
     "token": "your_jwt_token_here",
     "Total Protein": "7.0 g/dL",
     "Albumin": "4.5 g/dL",
     "Globulin": "2.5 g/dL",
     "A/G Ratio": "1.8",
     "Total Bilirubin": "0.8 mg/dL",
     "Direct Bilirubin": "0.2 mg/dL",
     "Indirect Bilirubin": "0.6 mg/dL",
     "AST (SGOT)": "25 U/L",
     "ALT (SGPT)": "30 U/L",
     "Alkaline Phosphatase": "90 U/L",
     "GGT": "20 U/L"
   }'
   ```

3. **Retrieve liver function test results:**
   ```bash
   curl -X POST http://127.0.0.1:8000/liver-function-test/get/ \
   -H "Content-Type: application/json" \
   -d '{"token": "your_jwt_token_here"}'
   ```

## Notes

- All liver function test parameters are stored as strings to preserve the original format with units
- If a user already has liver function test data, the store endpoint will update the existing record
- The API follows the same authentication pattern as other medical test endpoints in the system
- All endpoints require JWT token authentication passed in the request body
- The endpoints follow the same structure as the existing blood-test and metabolic-panel endpoints for consistency