# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Stack: Python 3 + Django 5 + Django REST Framework, JWT auth (djangorestframework-simplejwt), sqlite3 for dev, dotenv for environment.
- Entry points:
  - Django project: nexus/ (settings, urls, wsgi/asgi)
  - Application: nexusapp/ (models, serializers, views, urls)
  - API is mounted under /api/ (see nexus/urls.py includes nexusapp.urls)
- External integration: USDA FoodData Central API via settings.USDA_API_KEY.

Environment setup (Windows PowerShell)
- Create and activate a virtualenv
  - python -m venv .venv
  - .\.venv\Scripts\Activate.ps1
- Install dependencies
  - pip install -r requirements.txt
- Environment configuration
  - Ensure a .env exists at repo root with USDA_API_KEY set (SECRET_KEY has a dev default).

Run the app
- Apply migrations
  - python manage.py migrate
- (If you changed models) generate new migrations
  - python manage.py makemigrations
  - python manage.py migrate
- Create a superuser (optional, for admin)
  - python manage.py createsuperuser
- Start the dev server
  - python manage.py runserver
  - Optional (bind to all interfaces): python manage.py runserver 0.0.0.0:8000
- API base URL during local dev: http://127.0.0.1:8000/api

Public hosting with ngrok
- Install ngrok: winget install ngrok
- Start Django server: python manage.py runserver
- In another terminal, expose server: ngrok http 8000
- Use the provided HTTPS URL for public API access
- Note: Update CORS settings in nexus/settings.py if needed for production domains

Authentication (JWT)
- Token endpoints (provided by SimpleJWT and wired in nexusapp/urls.py):
  - POST /api/token/ (obtain access + refresh)
  - POST /api/token/refresh/ (refresh access)
- Note on authorization usage:
  - Although DRF is configured for header-based JWT ("Authorization: Bearer ..."), the current views expect a token field in the POST body for protected endpoints. Obtain the access token via /api/token/ and pass it as token in request bodies.
- Example: obtain token, then call a protected endpoint
  - Obtain token:
    curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d "{\"username\":\"alice\",\"password\":\"password\"}"
  - Use token in body (example: get basic info):
    curl -X POST http://127.0.0.1:8000/api/basic-info/get/ -H "Content-Type: application/json" -d "{\"token\":\"<ACCESS_TOKEN>\"}"

Testing and demo scripts
- Demo HTTP scripts (not Django unit tests):
  - Run a single script
    - python test_api.py
    - python test_jwt_api.py
    - python test_basic_info.py
    - python test_nutrition_goals.py
    - python test_post_summary.py
  - Ensure the dev server is running before executing these scripts; scripts target http://127.0.0.1:8000 by default.
- Django test runner (minimal/no unit tests in this repo)
  - python manage.py test

Common development commands
- Install deps: pip install -r requirements.txt
- Run server: python manage.py runserver
- Migrations: python manage.py makemigrations && python manage.py migrate
- Create admin user: python manage.py createsuperuser
- Run one demo script: python test_api.py (or any test_*.py script)
- Lint: None configured in this repository (no flake8/ruff/pylint in requirements.txt).

Architecture (high level)
- Routing
  - nexus/urls.py mounts admin at /admin/ and API at /api/ (include('nexusapp.urls')).
  - nexusapp/urls.py defines endpoints for:
    - Auth: POST /register/, POST /login/, POST /token/, POST /token/refresh/
    - User profiles: POST /basic-info/store/, POST /basic-info/get/
    - Health profile: POST /health-profile/store/, POST /health-profile/get/
    - Blood tests: POST /blood-test/store/, POST /blood-test/get/
    - Nutrition: POST /nutrition/, POST /nutrition/history/, POST /nutrition/goals/, POST /nutrition/summary/
- Views (nexusapp/views.py)
  - Function-based DRF views using @api_view and Response.
  - Auth pattern: endpoints expect a token in the request body; validated via JWTAuthentication to resolve the User.
  - Nutrition flow: queries USDA for item -> fetches nutrient details -> maps core macros -> converts units -> stores a FoodNutrition row -> returns per-100g and computed totals for requested quantity.
  - Goals sync: on storing UserHealthProfile, UserNutritionGoals are created/updated from daily_calorie_goal/daily_protein_goal defaults if present.
- Models (nexusapp/models.py)
  - UserBasicData: one-to-one with auth.User; demographics/contact.
  - UserHealthProfile: one-to-one; medical context, daily goals, and flattened emergency contact fields.
  - BloodTestReport: one-to-one; CBC fields plus metadata.
  - UserNutritionGoals: one-to-one; daily macro targets (calories, protein, carbs, fat, fiber, sugar).
  - FoodNutrition: per-entry macronutrients (per 100g), unit conversion, calculated totals in save(), and get_daily_totals(user, date) to aggregate consumption.
- Serialization (nexusapp/serializers.py)
  - UserSerializer wraps User creation (create_user), password write-only.
  - Model serializers for the above; UserHealthProfileSerializer flattens emergency_contact into *_name/relationship/phone and exposes a composite field for reads.
  - FoodNutritionSerializer exposes username read-only and marks derived totals/timestamps read-only.
  - Simple serializers structure responses for daily summary.
- Settings (nexus/settings.py)
  - INSTALLED_APPS includes rest_framework, rest_framework_simplejwt, corsheaders, nexusapp.
  - REST_FRAMEWORK DEFAULT_AUTHENTICATION_CLASSES uses SimpleJWT.
  - SIMPLE_JWT access lifetime 60m, refresh 1d; CORS allows http://localhost:3000 and http://127.0.0.1:3000.
  - Environment loaded from .env; USDA_API_KEY must be set for nutrition endpoints.

Operational notes
- Database: default sqlite3 at db.sqlite3 (local dev). Migrations under nexusapp/migrations/.
- Admin: /admin/ (requires superuser) is useful to inspect FoodNutrition and profile records.
- USDA API: Missing or invalid USDA_API_KEY will cause nutrition endpoints to fail.
