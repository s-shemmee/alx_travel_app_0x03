# ALX Travel App - Milestone 2

## Database Modeling and Data Seeding in Django

This project implements the database models, serializers, and management commands for the ALX Travel App.

## Features Implemented

### 🏗️ Database Models

**1. Listing Model**
- `listing_id`: UUID primary key
- `host`: Foreign key to User model
- `name`: Property name (max 200 characters)
- `description`: Detailed property description
- `location`: Property location (max 200 characters)
- `pricepernight`: Decimal field for nightly rate
- `created_at` & `updated_at`: Automatic timestamps

**2. Booking Model**
- `booking_id`: UUID primary key
- `property`: Foreign key to Listing model
- `user`: Foreign key to User model
- `start_date` & `end_date`: Booking date range
- `total_price`: Calculated total cost
- `created_at`: Automatic timestamp
- Constraints: End date must be after start date, no overlapping bookings

**3. Review Model**
- `review_id`: UUID primary key
- `property`: Foreign key to Listing model
- `user`: Foreign key to User model
- `rating`: Integer field (1-5 stars)
- `comment`: Review text
- `created_at`: Automatic timestamp
- Constraint: One review per user per property

### 🔄 API Serializers

**1. ListingSerializer**
- Full CRUD serialization for Listing model
- Nested host information (read-only)
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

## 🚀 Setup and Installation

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

## 📋 Completed Tasks

✅ **Database Models**: Listing, Booking, and Review models with proper relationships and constraints  
✅ **Serializers**: Complete DRF serializers with validation for all models  
✅ **Management Command**: Flexible seeder with customizable data generation  
✅ **Database Migration**: Successfully applied all model migrations  
✅ **Data Seeding**: Verified sample data creation and relationships  
✅ **Documentation**: Comprehensive README with setup instructions  

## 🚀 Next Steps

- Implement API views and endpoints
- Add authentication and permissions
- Create frontend integration
- Add advanced filtering and search
- Implement booking conflict resolution
- Add file upload for property images

---

**Project Status**: ✅ Milestone 2 Complete  
**Django Version**: 5.2.4  
**DRF Version**: 3.16.0  
**Database**: SQLite (Development)
