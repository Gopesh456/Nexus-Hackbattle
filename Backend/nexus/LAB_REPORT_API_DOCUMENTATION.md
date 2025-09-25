# Lab Report Management API Documentation

## Overview
The Lab Report Management API allows users to store and retrieve medical lab reports as base64-encoded files. The system supports various file types including PDFs, images, and documents, and provides secure storage with JWT authentication.

## Base URL
```
http://127.0.0.1:8000/api
```

## Authentication
All endpoints require JWT authentication. Include the JWT token in the request body as shown in the examples below.

---

## Endpoints

### 1. Store Lab Report
Store a new lab report with base64-encoded file data.

**URL:** `/lab-reports/store/`  
**Method:** `POST`  
**Authentication:** Required (JWT Token)

#### Request Body
```json
{
  "token": "your_jwt_token_here",
  "report_name": "Blood Test Report - September 2025",
  "report_type": "blood_test",
  "lab_name": "City Medical Laboratory",
  "doctor_name": "Dr. Sarah Smith",
  "report_date": "2025-09-25",
  "file_data": "base64_encoded_file_data_here",
  "file_name": "blood_test_report_sept_2025.pdf",
  "file_type": "pdf",
  "notes": "Routine annual blood work. All values normal."
}
```

#### Field Descriptions
| Field | Type | Required | Description | Example Values |
|-------|------|----------|-------------|----------------|
| `token` | string | Yes | JWT authentication token | "eyJ0eXAiOiJKV1QiLCJ..." |
| `report_name` | string | Yes | Descriptive name for the report | "Blood Test Report - Sept 2025" |
| `report_type` | string | Yes | Type of lab report | "blood_test", "x_ray", "mri" |
| `lab_name` | string | No | Name of the laboratory | "City Medical Laboratory" |
| `doctor_name` | string | No | Name of requesting doctor | "Dr. Sarah Smith" |
| `report_date` | string | Yes | Report date (YYYY-MM-DD format) | "2025-09-25" |
| `file_data` | string | Yes | Base64 encoded file content | "JVBERi0xLjQKMSAwIG9..." |
| `file_name` | string | Yes | Original filename with extension | "blood_test_report.pdf" |
| `file_type` | string | Yes | File extension (without dot) | "pdf", "jpg", "png" |
| `notes` | string | No | Additional notes about report | "Routine checkup results" |

#### Report Types
- **`blood_test`**: Blood Test Reports
- **`urine_test`**: Urine Test Reports  
- **`x_ray`**: X-Ray Images
- **`mri`**: MRI Scan Reports
- **`ct_scan`**: CT Scan Reports
- **`ultrasound`**: Ultrasound Reports
- **`ecg`**: ECG/EKG Reports
- **`pathology`**: Pathology Reports
- **`other`**: Other Types

#### Supported File Types
- **Documents**: pdf, doc, docx
- **Images**: jpg, jpeg, png, gif, bmp, tiff
- **Maximum file size**: 10MB

#### Success Response (201 Created)
```json
{
  "message": "Lab report stored successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "report_name": "Blood Test Report - September 2025",
    "report_type": "blood_test",
    "lab_name": "City Medical Laboratory",
    "doctor_name": "Dr. Sarah Smith",
    "report_date": "2025-09-25",
    "file_name": "blood_test_report_sept_2025.pdf",
    "file_type": "pdf",
    "file_size": 2048576,
    "file_size_mb": 2.05,
    "is_image": false,
    "is_pdf": true,
    "notes": "Routine annual blood work. All values normal.",
    "created_at": "2025-09-25T17:30:00Z",
    "updated_at": "2025-09-25T17:30:00Z"
  },
  "file_stored": true,
  "base64_length": 2731072
}
```

#### Error Responses
**401 Unauthorized - Missing Token**
```json
{
  "error": "Token is required"
}
```

**400 Bad Request - Invalid Base64**
```json
{
  "error": "Invalid data provided",
  "details": {
    "file_data": ["Invalid base64 data"]
  }
}
```

**400 Bad Request - File Too Large**
```json
{
  "error": "Invalid data provided",
  "details": {
    "file_data": ["File size cannot exceed 10MB"]
  }
}
```

---

### 2. Get All Lab Reports
Retrieve all lab reports for the authenticated user (metadata only by default).

**URL:** `/lab-reports/get/`  
**Method:** `POST`  
**Authentication:** Required (JWT Token)

#### Request Body
```json
{
  "token": "your_jwt_token_here",
  "include_file_data": false
}
```

#### Parameters
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `token` | string | Yes | JWT authentication token | - |
| `include_file_data` | boolean | No | Include base64 file data in response | false |

#### Success Response (200 OK)
```json
{
  "user": "john_doe",
  "count": 2,
  "reports": [
    {
      "id": 2,
      "username": "john_doe",
      "report_name": "X-Ray Chest - September 2025",
      "report_type": "x_ray",
      "lab_name": "Radiology Center",
      "doctor_name": "Dr. Michael Brown",
      "report_date": "2025-09-20",
      "file_name": "chest_xray_sept_2025.jpg",
      "file_type": "jpg",
      "file_size": 1536000,
      "file_size_mb": 1.54,
      "is_image": true,
      "is_pdf": false,
      "notes": "Chest X-ray for routine examination",
      "created_at": "2025-09-25T17:25:00Z",
      "updated_at": "2025-09-25T17:25:00Z"
    },
    {
      "id": 1,
      "username": "john_doe",
      "report_name": "Blood Test Report - September 2025",
      "report_type": "blood_test",
      "lab_name": "City Medical Laboratory",
      "doctor_name": "Dr. Sarah Smith",
      "report_date": "2025-09-25",
      "file_name": "blood_test_report_sept_2025.pdf",
      "file_type": "pdf",
      "file_size": 2048576,
      "file_size_mb": 2.05,
      "is_image": false,
      "is_pdf": true,
      "notes": "Routine annual blood work. All values normal.",
      "created_at": "2025-09-25T17:30:00Z",
      "updated_at": "2025-09-25T17:30:00Z"
    }
  ],
  "note": "File data excluded for performance. Set include_file_data=true to include base64 data."
}
```

---

### 3. Get Specific Lab Report File
Retrieve the base64 file data for a specific lab report.

**URL:** `/lab-reports/file/`  
**Method:** `POST`  
**Authentication:** Required (JWT Token)

#### Request Body
```json
{
  "token": "your_jwt_token_here",
  "report_id": 1
}
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `token` | string | Yes | JWT authentication token |
| `report_id` | integer | Yes | ID of the lab report |

#### Success Response (200 OK)
```json
{
  "report_id": 1,
  "report_name": "Blood Test Report - September 2025",
  "file_name": "blood_test_report_sept_2025.pdf",
  "file_type": "pdf",
  "file_size": 2048576,
  "file_size_mb": 2.05,
  "file_data": "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXM...",
  "is_image": false,
  "is_pdf": true
}
```

#### Error Responses
**404 Not Found - Report Not Found**
```json
{
  "error": "Lab report not found or you do not have permission to access it"
}
```

---

## Usage Examples

### JavaScript/Frontend Integration
```javascript
class LabReportAPI {
  constructor(baseURL = 'http://127.0.0.1:8000/api') {
    this.baseURL = baseURL;
  }

  // Convert file to base64
  fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        // Remove data URL prefix (data:type/subtype;base64,)
        const base64 = reader.result.split(',')[1];
        resolve(base64);
      };
      reader.onerror = error => reject(error);
    });
  }

  // Store lab report
  async storeLabReport(token, reportData, file) {
    try {
      const base64Data = await this.fileToBase64(file);
      
      const payload = {
        token: token,
        ...reportData,
        file_data: base64Data,
        file_name: file.name,
        file_type: file.name.split('.').pop().toLowerCase()
      };

      const response = await fetch(`${this.baseURL}/lab-reports/store/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to store lab report');
      }

      return await response.json();
    } catch (error) {
      console.error('Error storing lab report:', error);
      throw error;
    }
  }

  // Get all lab reports
  async getLabReports(token, includeFileData = false) {
    const response = await fetch(`${this.baseURL}/lab-reports/get/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        token, 
        include_file_data: includeFileData 
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to retrieve lab reports');
    }

    return await response.json();
  }

  // Get specific lab report file
  async getLabReportFile(token, reportId) {
    const response = await fetch(`${this.baseURL}/lab-reports/file/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token, report_id: reportId })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to retrieve lab report file');
    }

    return await response.json();
  }

  // Download file from base64
  downloadFromBase64(base64Data, fileName, fileType) {
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: this.getMimeType(fileType) });
    
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  getMimeType(fileType) {
    const mimeTypes = {
      'pdf': 'application/pdf',
      'jpg': 'image/jpeg',
      'jpeg': 'image/jpeg',
      'png': 'image/png',
      'gif': 'image/gif',
      'doc': 'application/msword',
      'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    };
    return mimeTypes[fileType.toLowerCase()] || 'application/octet-stream';
  }
}

// Usage Example
const labAPI = new LabReportAPI();

// Store lab report with file upload
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  
  const reportData = {
    report_name: document.getElementById('reportName').value,
    report_type: document.getElementById('reportType').value,
    lab_name: document.getElementById('labName').value,
    doctor_name: document.getElementById('doctorName').value,
    report_date: document.getElementById('reportDate').value,
    notes: document.getElementById('notes').value
  };

  try {
    const result = await labAPI.storeLabReport('your_jwt_token', reportData, file);
    console.log('Lab report stored:', result);
  } catch (error) {
    console.error('Error:', error.message);
  }
});
```

### Python/Backend Integration
```python
import requests
import base64
import json
from datetime import date

class LabReportClient:
    def __init__(self, base_url='http://127.0.0.1:8000/api'):
        self.base_url = base_url
    
    def file_to_base64(self, file_path):
        """Convert file to base64 string"""
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                base64_data = base64.b64encode(content).decode('utf-8')
                return base64_data
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
    
    def store_lab_report(self, token, report_data, file_path):
        """Store lab report with file"""
        try:
            # Convert file to base64
            base64_data = self.file_to_base64(file_path)
            
            # Get file info
            import os
            file_name = os.path.basename(file_path)
            file_type = file_name.split('.')[-1].lower()
            
            # Prepare payload
            payload = {
                'token': token,
                **report_data,
                'file_data': base64_data,
                'file_name': file_name,
                'file_type': file_type
            }
            
            # Send request
            url = f"{self.base_url}/lab-reports/store/"
            response = requests.post(url, json=payload)
            
            return response.json()
            
        except Exception as e:
            raise Exception(f"Error storing lab report: {e}")
    
    def get_lab_reports(self, token, include_file_data=False):
        """Get all lab reports"""
        url = f"{self.base_url}/lab-reports/get/"
        data = {
            'token': token,
            'include_file_data': include_file_data
        }
        
        response = requests.post(url, json=data)
        return response.json()
    
    def get_lab_report_file(self, token, report_id):
        """Get specific lab report file"""
        url = f"{self.base_url}/lab-reports/file/"
        data = {
            'token': token,
            'report_id': report_id
        }
        
        response = requests.post(url, json=data)
        return response.json()
    
    def save_base64_to_file(self, base64_data, output_path):
        """Save base64 data to file"""
        try:
            decoded_data = base64.b64decode(base64_data)
            with open(output_path, 'wb') as file:
                file.write(decoded_data)
            print(f"File saved to: {output_path}")
        except Exception as e:
            raise Exception(f"Error saving file: {e}")

# Usage Example
client = LabReportClient()

# Store lab report
report_data = {
    'report_name': 'Blood Test Report - September 2025',
    'report_type': 'blood_test',
    'lab_name': 'City Medical Laboratory',
    'doctor_name': 'Dr. Sarah Smith',
    'report_date': '2025-09-25',
    'notes': 'Routine annual blood work'
}

try:
    # Store report with file
    result = client.store_lab_report(
        token='your_jwt_token',
        report_data=report_data,
        file_path='/path/to/lab_report.pdf'
    )
    print("Stored report:", result)
    
    # Get all reports
    reports = client.get_lab_reports('your_jwt_token')
    print("All reports:", reports)
    
    # Get specific file
    if reports['count'] > 0:
        report_id = reports['reports'][0]['id']
        file_data = client.get_lab_report_file('your_jwt_token', report_id)
        
        # Save file locally
        client.save_base64_to_file(
            file_data['file_data'],
            f"downloaded_{file_data['file_name']}"
        )
        
except Exception as e:
    print(f"Error: {e}")
```

---

## Security Considerations

1. **File Size Limits**: Maximum 10MB per file to prevent server overload
2. **File Type Validation**: Only specific file types are allowed
3. **Base64 Validation**: All base64 data is validated before storage
4. **JWT Authentication**: All endpoints require valid JWT tokens
5. **User Isolation**: Users can only access their own lab reports
6. **Sensitive Data**: Base64 file data is excluded from list responses by default

---

## Best Practices

1. **File Optimization**: Compress files before encoding to base64
2. **Error Handling**: Always implement proper error handling for file operations
3. **Progress Indicators**: Show upload progress for large files
4. **Caching**: Consider caching frequently accessed reports
5. **Backup**: Implement regular backups for stored lab reports
6. **Audit Trail**: Log all file access and modifications
7. **Storage Management**: Monitor storage usage and implement cleanup policies

---

## Database Schema

The `LabReport` model stores the following information:

```sql
CREATE TABLE nexusapp_labreport (
    id BIGINT PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id),
    report_name VARCHAR(255),
    report_type VARCHAR(50),
    lab_name VARCHAR(255),
    doctor_name VARCHAR(255),
    report_date DATE,
    report_file_base64 TEXT,  -- Base64 file data stored here
    file_name VARCHAR(255),
    file_type VARCHAR(10),
    file_size INTEGER,
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

The base64 file data is stored directly in the database as text, allowing for easy retrieval and manipulation while maintaining data integrity.