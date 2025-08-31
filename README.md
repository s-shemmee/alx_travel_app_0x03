# Milestone 5: Celery & Email Notification Setup

## Celery Configuration
- Celery is configured with RabbitMQ as the broker.
- See `settings.py` for broker and backend settings.
- Celery app is initialized in `celery.py`.

## Email Notification Task
- The shared task for sending booking confirmation emails is in `apps/listings/tasks.py`.
- Booking creation triggers the email task asynchronously via Celery in `BookingViewSet`.

## How to Run
1. Start RabbitMQ server (locally or remotely).
2. Start Celery worker:
   ```bash
   celery -A celery worker --loglevel=info
   ```
3. Run Django server as usual.

## Testing
- Create a booking via API or admin.
- Check that a confirmation email is sent asynchronously.

## Configuration
- Update SMTP settings in `settings.py` for your email provider.

## Files Modified
- `settings.py`: Celery & email config
- `celery.py`: Celery app
- `apps/listings/tasks.py`: Email task
- `apps/listings/views.py`: Task trigger

---
For manual review, ensure RabbitMQ and Celery worker are running, and test booking creation for email delivery.
# ALX Travel App - Milestone 3

## API Development for Listings and Bookings in Django

This project implements ViewSets and API endpoints for managing listings and bookings, with comprehensive API documentation using Swagger.

## Features Implemented

### 🏗️ Database Models


- `listing_id`: UUID primary key
- `host`: Foreign key to User model
- `name`: Property name (max 200 characters)
- `description`: Detailed property description
- `location`: Property location (max 200 characters)
- `property`: Foreign key to Listing model
- `user`: Foreign key to User model
- `total_price`: Calculated total cost
- `created_at`: Automatic timestamp
**3. Review Model**
- `review_id`: UUID primary key
- `rating`: Integer field (1-5 stars)
- `comment`: Review text

**1. ListingSerializer**
- Price validation (must be positive)
- Host assignment via `host_id` field

**2. BookingSerializer**
- Full CRUD serialization for Booking model
- Nested property and user information (read-only)
- Date validation (end date after start date)
- Overlapping booking prevention
- Price validation (must be positive)

**3. ReviewSerializer**
- Full CRUD serialization for Review model
- Nested property and user information (read-only)
- Rating validation (1-5 range)
- One review per user per property constraint

**4. UserSerializer**
- Basic user information serialization
- Fields: id, username, first_name, last_name, email

### 🌱 Database Seeding

**Management Command: `python manage.py seed`**

Options:
- `--users <number>`: Number of users to create (default: 10)
- `--listings <number>`: Number of listings to create (default: 20)
- `--bookings <number>`: Number of bookings to create (default: 15)
- `--reviews <number>`: Number of reviews to create (default: 25)

**Sample Data Generated:**
- **Users**: Random names with realistic email addresses
- **Listings**: Various property types (Apartment, House, Villa, etc.) across major US cities
- **Bookings**: Non-overlapping reservations with calculated pricing
- **Reviews**: Realistic ratings (biased toward 4-5 stars) with sample comments

## � API Endpoints (Milestone 3)

The following RESTful endpoints are available under `/api/`:

### Listings API
- `GET /api/listings/` — List all listings
- `POST /api/listings/` — Create a new listing
- `GET /api/listings/{id}/` — Retrieve a listing
- `PUT /api/listings/{id}/` — Update a listing
- `DELETE /api/listings/{id}/` — Delete a listing

### Bookings API
- `GET /api/bookings/` — List all bookings
- `POST /api/bookings/` — Create a new booking
- `GET /api/bookings/{id}/` — Retrieve a booking
- `PUT /api/bookings/{id}/` — Update a booking
- `DELETE /api/bookings/{id}/` — Delete a booking

### API Documentation

Interactive Swagger UI is available at: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

You can use tools like Postman or the Swagger UI to test all endpoints (GET, POST, PUT, DELETE).

## �🚀 Setup and Installation

### Prerequisites
- Python 3.13+
- Django 5.2.4
- Virtual environment

### Installation Steps

1. **Activate Virtual Environment**
   ```bash
   source .venv/Scripts/activate  # Windows
   # or
   source .venv/bin/activate      # Linux/Mac
   ```

2. **Install Dependencies**
   ```bash
   pip install Django==5.2.4
   pip install djangorestframework==3.16.0
   pip install django-cors-headers==4.7.0
   pip install drf-yasg==1.21.10
   ```

3. **Apply Migrations**
   ```bash
   cd alx_travel_app
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Seed Database**
   ```bash
   python manage.py seed
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## 📁 Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app/
│   ├── manage.py
│   ├── db.sqlite3
│   └── alx_travel_app/
│       ├── settings.py
│       ├── urls.py
│       └── listings/
│           ├── models.py          # Database models
│           ├── serializers.py     # DRF serializers
│           ├── management/
│           │   └── commands/
│           │       └── seed.py    # Database seeder
│           └── migrations/
│               └── 0001_initial.py
└── README.md
```

## 🔧 Key Features

### Model Relationships
- **One-to-Many**: User → Listings (host relationship)
- **One-to-Many**: User → Bookings (guest relationship)
- **One-to-Many**: User → Reviews (reviewer relationship)
- **One-to-Many**: Listing → Bookings
- **One-to-Many**: Listing → Reviews

### Validation Rules
- **Listings**: Positive pricing, required fields
- **Bookings**: Valid date ranges, no overlaps, positive pricing
- **Reviews**: Rating range (1-5), unique per user-property pair

### Database Constraints
- UUID primary keys for all main models
- Automatic timestamp management
- Foreign key relationships with cascading deletes
- Check constraints for data integrity

## 🎯 Testing the Implementation

### Verify Database Seeding
```bash
python manage.py seed --users 5 --listings 10 --bookings 5 --reviews 8
```

### Check API Endpoints
- Root: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- API: `http://127.0.0.1:8000/api/`
- Swagger: `http://127.0.0.1:8000/swagger/`

## 📋 Completed Tasks (Milestone 3)

✅ **Database Models**: Listing, Booking, and Review models with proper relationships and constraints  
✅ **Serializers**: Complete DRF serializers with validation for all models  
✅ **Management Command**: Flexible seeder with customizable data generation  
✅ **Database Migration**: Successfully applied all model migrations  
✅ **Data Seeding**: Verified sample data creation and relationships  
✅ **API Views**: ViewSets for Listing and Booking with full CRUD operations  
✅ **REST URLs**: Router-based URL configuration under `/api/`  
✅ **API Tests**: Unit tests for API endpoints  
✅ **Swagger Documentation**: Interactive API documentation available  
✅ **Documentation**: Comprehensive README with setup instructions  

## 🚀 Next Steps

- Implement API views and endpoints
- Add authentication and permissions
- Create frontend integration
- Add advanced filtering and search
- Implement booking conflict resolution
- Add file upload for property images

---

**Project Status**: ✅ Milestone 3 Complete  
**Django Version**: 5.2.4  
**DRF Version**: 3.16.0  
**Database**: SQLite (Development)  
**API Endpoints**: ✅ Functional with Swagger Documentation
