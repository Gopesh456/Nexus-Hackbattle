# Nexus-Hackbattle: Food Nutrition Tracker

A full-stack application that fetches nutritional information from the USDA FoodData Central API and stores it in a database.

## 🚀 Features

- **Food Nutrition API**: POST endpoint to get nutritional data for any food item
- **USDA Integration**: Fetches accurate nutrition data from USDA FoodData Central
- **Data Storage**: Stores all nutrition information in Django database
- **Macro Nutrients**: Returns calories, protein, carbohydrates, fat, fiber, and sugar
- **Quantity Calculation**: Automatically calculates nutrition for specified quantity
- **History Tracking**: Stores and retrieves nutrition history

## 🛠 Tech Stack

**Backend:**
- Django 5.2.6
- Django REST Framework
- SQLite Database
- USDA FoodData Central API

**Frontend:**
- HTML5/CSS3/JavaScript
- Fetch API for HTTP requests
- Responsive design

## 📁 Project Structure

```
Nexus-Hackbattle/
├── Backend/
│   └── nexus/
│       ├── manage.py
│       ├── requirements.txt
│       ├── .env (create this)
│       ├── API_DOCUMENTATION.md
│       ├── test_api.py
│       ├── nexus/
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── ...
│       └── nexusapp/
│           ├── models.py (FoodNutrition model)
│           ├── views.py (nutrition endpoints)
│           ├── serializers.py
│           └── ...
├── Frontend/
│   ├── test_nutrition_api.html (demo page)
│   └── nexus/ (Next.js app)
└── README.md
```

## 🔧 Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/Gopesh456/Nexus-Hackbattle.git
cd Nexus-Hackbattle
```

### 2. Backend Setup
```bash
cd Backend/nexus

# Create virtual environment (if not exists)
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in `Backend/nexus/`:
```
USDA_API_KEY=your_usda_api_key_here
SECRET_KEY=django-insecure-w#201%sc097y5kpxlg&^_k&1j79o#=z6qwzdvdbkv4h19ll&+4
```

**Get USDA API Key:**
1. Visit https://fdc.nal.usda.gov/api-guide.html
2. Sign up for free API access
3. Add your API key to the `.env` file

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run Server
```bash
python manage.py runserver
```
Server will run at http://127.0.0.1:8000/

## � Authentication

The API uses **JWT (JSON Web Token)** authentication. Users must register/login to access their personal food diary.

## �📊 API Endpoints

### Authentication Endpoints

**POST /api/register/** - Register new user
**POST /api/login/** - Login and get JWT tokens
**POST /api/token/refresh/** - Refresh access token

### Protected Endpoints (Require JWT Token)

### POST /api/nutrition/
Get nutrition data for a food item and store it for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_access_token>
Content-Type: application/json
```

**Request:**
```json
{
    "food_name": "apple",
    "quantity": 150
}
```

**Response:**
```json
{
    "food_name": "apple",
    "quantity": 150,
    "unit": "grams",
    "nutrition_per_100g": {
        "calories": 52.0,
        "protein": 0.26,
        "carbohydrates": 13.81,
        "fat": 0.17,
        "fiber": 2.4,
        "sugar": 10.39
    },
    "total_nutrition": {
        "calories": 78.0,
        "protein": 0.39,
        "carbohydrates": 20.72,
        "fat": 0.26,
        "fiber": 3.6,
        "sugar": 15.59
    },
    "usda_food_name": "Apples, raw, with skin",
    "stored_id": 1
}
```

### GET /api/nutrition/history/
Get authenticated user's food diary history (latest 50 records).

**Headers:**
```
Authorization: Bearer <jwt_access_token>
```

## 🖥 Frontend Integration

### Test Page
Open `Frontend/test_nutrition_api.html` in your browser to test the API with a simple web interface.

### React/Next.js Integration with JWT
```javascript
// Login and get JWT token
const login = async (username, password) => {
    const response = await fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    localStorage.setItem('access_token', data.tokens.access);
    return data;
};

// Add food entry with authentication
const getNutritionData = async (foodName, quantity) => {
    const token = localStorage.getItem('access_token');
    const response = await fetch('http://127.0.0.1:8000/api/nutrition/', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ food_name: foodName, quantity })
    });
    return await response.json();
};
```

## 🗄 Database Schema

**FoodNutrition Model:**
- user: ForeignKey to User (links entries to specific users)
- food_name: CharField
- quantity: FloatField
- usda_food_id: CharField
- Nutrition per 100g: calories, protein, carbs, fat, fiber, sugar
- Total nutrition: calculated values for specified quantity
- created_at: DateTimeField

## 🧪 Testing

### Test JWT Authentication API
```bash
python test_jwt_api.py
```

### Test Basic API (Legacy)
```bash
python test_api.py
```

### Manual Testing
1. Start Django server: `python manage.py runserver`
2. Open `Frontend/test_nutrition_api.html` in browser
3. Enter food name and quantity
4. View nutrition results

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **User Data Isolation**: Each user can only access their own food entries
- **Token Expiry**: Access tokens expire in 60 minutes for security
- **Refresh Tokens**: 7-day refresh token lifecycle
- **CORS Protection**: Configured for localhost:3000 (React/Next.js)
- **USDA API Key**: Stored securely in environment variables
- **Input Validation**: Server-side validation on all inputs

## 📚 Documentation

- **JWT API Documentation**: `Backend/nexus/JWT_API_DOCUMENTATION.md` ⭐
- **Legacy API Documentation**: `Backend/nexus/API_DOCUMENTATION.md`
- **Database Models**: `Backend/nexus/nexusapp/models.py`
- **API Views**: `Backend/nexus/nexusapp/views.py`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

**Common Issues:**

1. **USDA API Key Error**: Make sure you have a valid API key in `.env`
2. **CORS Error**: Ensure CORS is configured for your frontend URL
3. **Database Error**: Run migrations: `python manage.py migrate`
4. **Module Import Error**: Activate virtual environment and install requirements

**Need Help?**
- Check API documentation in `Backend/nexus/API_DOCUMENTATION.md`
- Run test script: `python test_api.py`
- Open browser console for frontend debugging