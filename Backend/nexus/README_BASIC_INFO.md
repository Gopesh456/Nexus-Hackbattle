# Basic_Info Model and API Documentation

This document provides comprehensive documentation for the `Basic_Info` model and its associated REST API endpoints for storing and managing user basic information.

## Model Overview

The `Basic_Info` model stores essential user information in the exact format specified:

```python
{
    "full_name": "string",
    "date_of_birth": "yyyy-mm-dd", 
    "gender": "string",
    "location": "string",
    "email": "string",
    "phone": "string"
}
```

## Database Schema

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | AutoField | Primary Key | Auto-generated unique identifier |
| `full_name` | CharField(255) | Required | User's full name |
| `date_of_birth` | DateField | Required | Date of birth in YYYY-MM-DD format |
| `gender` | CharField(20) | Choices | Gender: male, female, other, prefer_not_to_say |
| `location` | CharField(255) | Required | User's location/address |
| `email` | EmailField | Unique, Required | User's email address |
| `phone` | CharField(17) | Validated | Phone number with country code |
| `created_at` | DateTimeField | Auto-generated | Record creation timestamp |
| `updated_at` | DateTimeField | Auto-updated | Record last update timestamp |

### Model Features

- **Age Calculation**: Automatic age calculation from date of birth
- **Email Uniqueness**: Prevents duplicate email addresses
- **Phone Validation**: Validates phone number format (9-15 digits)
- **Date Validation**: Prevents future dates and unrealistic ages (>120 years)
- **Metadata Tracking**: Automatic timestamps for creation and updates

## API Endpoints

### Base URL
```
http://127.0.0.1:8000/api
```

### Authentication
Most endpoints are currently set to `AllowAny` for testing. In production, you should implement proper authentication.

## CRUD Operations

### 1. Create Basic Info
**POST** `/basic-info/`

Creates a new basic information record.

**Request Body:**
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

**Response (201 Created):**
```json
{
    "message": "Basic information created successfully",
    "data": {
        "id": 1,
        "full_name": "John Doe",
        "date_of_birth": "1995-05-15",
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

### 2. Get All Basic Info Records
**GET** `/basic-info/all/`

Retrieves all basic information records.

**Response (200 OK):**
```json
{
    "count": 2,
    "data": [
        {
            "id": 1,
            "full_name": "John Doe",
            "date_of_birth": "1995-05-15",
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

### 3. Get Single Basic Info Record  
**GET** `/basic-info/{id}/`

Retrieves a specific basic information record by ID.

**Response (200 OK):**
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
        "age": 30,
        "created_at": "2025-09-24T15:30:00.000Z",
        "updated_at": "2025-09-24T15:30:00.000Z"
    }
}
```

### 4. Update Basic Info
**PUT/PATCH** `/basic-info/{id}/update/`

Updates an existing basic information record.
- **PUT**: Full update (all fields required)
- **PATCH**: Partial update (only modified fields required)

**Request Body (PATCH example):**
```json
{
    "location": "Los Angeles, USA",
    "phone": "+1987654321"
}
```

**Response (200 OK):**
```json
{
    "message": "Basic information updated successfully",
    "data": {
        "id": 1,
        "full_name": "John Doe",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "location": "Los Angeles, USA",
        "email": "john@example.com",
        "phone": "+1987654321",
        "age": 30,
        "created_at": "2025-09-24T15:30:00.000Z",
        "updated_at": "2025-09-24T15:35:00.000Z"
    }
}
```

### 5. Delete Basic Info
**DELETE** `/basic-info/{id}/delete/`

Deletes a basic information record.

**Response (200 OK):**
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

### 6. Search Basic Info
**GET** `/basic-info/search/`

Search basic information records using query parameters.

**Query Parameters:**
- `full_name`: Partial name search
- `email`: Exact email search  
- `location`: Partial location search
- `gender`: Exact gender search

**Example Request:**
```
GET /basic-info/search/?gender=female&location=USA
```

**Response (200 OK):**
```json
{
    "count": 1,
    "data": [
        {
            "id": 2,
            "full_name": "Jane Smith", 
            "date_of_birth": "1992-08-20",
            "gender": "female",
            "location": "Chicago, USA",
            "email": "jane@example.com",
            "phone": "+1555666777",
            "age": 33,
            "created_at": "2025-09-24T15:30:00.000Z",
            "updated_at": "2025-09-24T15:30:00.000Z"
        }
    ],
    "filters_applied": {
        "full_name": null,
        "email": null, 
        "location": "USA",
        "gender": "female"
    }
}
```

## Validation Rules

### Field Validations

1. **full_name**: 
   - Required
   - Maximum 255 characters

2. **date_of_birth**:
   - Required
   - Must be in YYYY-MM-DD format
   - Cannot be in the future
   - Age cannot exceed 120 years

3. **gender**:
   - Required
   - Must be one of: `male`, `female`, `other`, `prefer_not_to_say`

4. **location**:
   - Required
   - Maximum 255 characters

5. **email**:
   - Required
   - Must be valid email format
   - Must be unique across all records

6. **phone**:
   - Required
   - Must match regex pattern: `^\\+?1?\\d{9,15}$`
   - Allows international format with + prefix
   - Must be 9-15 digits long

### Error Response Format

**Validation Error (400 Bad Request):**
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

## Usage Examples

### Using cURL

#### Create a new record:
```bash
curl -X POST http://127.0.0.1:8000/api/basic-info/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Alice Johnson",
    "date_of_birth": "1988-12-03",
    "gender": "female",
    "location": "Seattle, WA",
    "email": "alice@example.com",
    "phone": "+1206555000"
  }'
```

#### Get all records:
```bash
curl -X GET http://127.0.0.1:8000/api/basic-info/all/
```

#### Update a record:
```bash
curl -X PATCH http://127.0.0.1:8000/api/basic-info/1/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Portland, OR",
    "phone": "+1503555111"
  }'
```

#### Search records:
```bash
curl -X GET "http://127.0.0.1:8000/api/basic-info/search/?gender=male&location=New%20York"
```

### Using Python requests

```python
import requests

# Create a new record
data = {
    "full_name": "Bob Wilson",
    "date_of_birth": "1985-03-22",
    "gender": "male",
    "location": "Boston, MA",
    "email": "bob@example.com",
    "phone": "+1617555222"
}

response = requests.post('http://127.0.0.1:8000/api/basic-info/', json=data)
print(response.json())

# Get all records  
response = requests.get('http://127.0.0.1:8000/api/basic-info/all/')
print(response.json())

# Search by gender
response = requests.get('http://127.0.0.1:8000/api/basic-info/search/', 
                       params={'gender': 'female'})
print(response.json())
```

## Django Admin Integration

The `Basic_Info` model is fully integrated with Django Admin:

### Admin Features:
- **List View**: Shows name, email, gender, location, age, and creation date
- **Search**: Search by name, email, and location
- **Filters**: Filter by gender, creation date, and date of birth
- **Date Hierarchy**: Navigate by date of birth
- **Fieldsets**: Organized form layout with collapsible metadata section
- **Read-only Fields**: Timestamps and calculated age

### Access Admin Panel:
```
http://127.0.0.1:8000/admin/nexusapp/basic_info/
```

## Testing

### Run the Test Script
```bash
# Install requests if not already installed
pip install requests

# Start the Django development server
python manage.py runserver

# In another terminal, run the test script
python test_basic_info.py
```

### Test Coverage
The test script covers:
- ✅ Creating records with valid data
- ✅ Retrieving all records
- ✅ Retrieving single records by ID  
- ✅ Updating records (PATCH)
- ✅ Searching with various filters
- ✅ Deleting records
- ✅ Validation error handling
- ✅ Age calculation
- ✅ Email uniqueness validation

## Database Operations

### Creating Records via Django ORM
```python
from nexusapp.models import Basic_Info
from datetime import date

# Create a new record
info = Basic_Info.objects.create(
    full_name="Emma Davis",
    date_of_birth=date(1993, 7, 15),
    gender="female",
    location="Austin, TX",
    email="emma@example.com",
    phone="+1512555333"
)

print(f"Created: {info}")
print(f"Age: {info.age}")
print(f"Dict format: {info.to_dict()}")
```

### Querying Records
```python
# Get all records
all_users = Basic_Info.objects.all()

# Filter by gender
females = Basic_Info.objects.filter(gender='female')

# Search by name (case-insensitive)
johns = Basic_Info.objects.filter(full_name__icontains='john')

# Get by email
user = Basic_Info.objects.get(email='emma@example.com')

# Order by creation date
recent = Basic_Info.objects.order_by('-created_at')
```

## Migration Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations  
python manage.py migrate

# Check migration status
python manage.py showmigrations nexusapp
```

## Security Considerations

### For Production:
1. **Authentication**: Add proper authentication to endpoints
2. **Rate Limiting**: Implement rate limiting for API endpoints
3. **Input Sanitization**: Add additional input validation
4. **HTTPS**: Use HTTPS in production
5. **CORS**: Configure CORS settings appropriately
6. **Database**: Use PostgreSQL or another production database

### Example Authentication Setup:
```python
# In views.py
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication
def create_basic_info(request):
    # ... implementation
```

## Performance Considerations

### Database Indexes
Consider adding database indexes for frequently queried fields:

```python
class Basic_Info(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['gender']), 
            models.Index(fields=['created_at']),
        ]
```

### Pagination
For large datasets, implement pagination:

```python
from django.core.paginator import Paginator

def get_basic_info(request, pk=None):
    if not pk:
        queryset = Basic_Info.objects.all().order_by('-created_at')
        paginator = Paginator(queryset, 20)  # 20 records per page
        # ... pagination logic
```

## Troubleshooting

### Common Issues:

1. **Email already exists error**:
   - Ensure email uniqueness across all records
   - Check for case sensitivity issues

2. **Phone validation fails**:
   - Ensure phone number includes country code
   - Format: +1234567890 or similar

3. **Date format errors**:
   - Use YYYY-MM-DD format only
   - Ensure date is not in the future

4. **Migration issues**:
   ```bash
   python manage.py migrate nexusapp zero  # Reset migrations
   python manage.py makemigrations nexusapp
   python manage.py migrate
   ```

## Future Enhancements

### Potential Improvements:
1. **Profile Pictures**: Add image upload functionality
2. **Address Validation**: Integrate with address validation APIs
3. **Social Links**: Add fields for social media profiles  
4. **Privacy Settings**: Add privacy controls for data visibility
5. **Data Export**: Add functionality to export user data
6. **Audit Trail**: Track all changes to user records
7. **Bulk Operations**: Add bulk create/update endpoints

This documentation provides a complete guide to using the Basic_Info model and API endpoints for managing user basic information in your Django application.