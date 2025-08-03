# Test API Endpoints with curl

## Test Listings API

### GET All Listings
curl -X GET http://127.0.0.1:8000/api/listings/

### POST Create Listing
curl -X POST http://127.0.0.1:8000/api/listings/ \
  -H "Content-Type: application/json" \
  -d '{
    "host_id": 1,
    "name": "Beautiful Beachfront Villa",
    "description": "A stunning villa with ocean views",
    "location": "Malibu, CA",
    "pricepernight": 350.00
  }'

### GET Single Listing (replace {id} with actual UUID)
curl -X GET http://127.0.0.1:8000/api/listings/{listing_uuid}/

### PUT Update Listing (replace {id} with actual UUID)
curl -X PUT http://127.0.0.1:8000/api/listings/{listing_uuid}/ \
  -H "Content-Type: application/json" \
  -d '{
    "host_id": 1,
    "name": "Updated Villa Name",
    "description": "Updated description",
    "location": "Updated Location",
    "pricepernight": 400.00
  }'

### DELETE Listing (replace {id} with actual UUID)
curl -X DELETE http://127.0.0.1:8000/api/listings/{listing_uuid}/

## Test Bookings API

### GET All Bookings
curl -X GET http://127.0.0.1:8000/api/bookings/

### POST Create Booking
curl -X POST http://127.0.0.1:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "{listing_uuid}",
    "user_id": 1,
    "start_date": "2025-08-15",
    "end_date": "2025-08-20",
    "total_price": 1750.00
  }'

### GET Single Booking (replace {id} with actual UUID)
curl -X GET http://127.0.0.1:8000/api/bookings/{booking_uuid}/

### PUT Update Booking (replace {id} with actual UUID)
curl -X PUT http://127.0.0.1:8000/api/bookings/{booking_uuid}/ \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "{listing_uuid}",
    "user_id": 1,
    "start_date": "2025-08-16",
    "end_date": "2025-08-21",
    "total_price": 1750.00
  }'

### DELETE Booking (replace {id} with actual UUID)
curl -X DELETE http://127.0.0.1:8000/api/bookings/{booking_uuid}/

## API Endpoints Summary

Available at: http://127.0.0.1:8000/api/

### Listings
- GET /api/listings/ - List all listings
- POST /api/listings/ - Create new listing
- GET /api/listings/{id}/ - Get specific listing
- PUT /api/listings/{id}/ - Update listing
- DELETE /api/listings/{id}/ - Delete listing

### Bookings
- GET /api/bookings/ - List all bookings
- POST /api/bookings/ - Create new booking
- GET /api/bookings/{id}/ - Get specific booking
- PUT /api/bookings/{id}/ - Update booking
- DELETE /api/bookings/{id}/ - Delete booking

### API Documentation
- Swagger UI: http://127.0.0.1:8000/swagger/
- Interactive testing available through Swagger interface
