# Booking System

## System Architecture
The Booking System follows a RESTful architecture with the following components:
- Backend: Python-based API server
- Database: PostgreSQL for data persistence
- Authentication: Token-based authentication system
- Docker: Containerization for easy deployment

## System Design

### Database Schema
1. **Resources**
   - id (Primary Key)
   - name (String)
   - description (Text)
   - total_quantity (Integer)
   - available_quantity (Integer)

2. **Bookings**
   - id (Primary Key)
   - resource_id (Foreign Key)
   - user_id (Foreign Key)
   - purchase_quantity (Integer)
   - booking_date (Timestamp with timezone)

3. **Users**
   - id (Primary Key)
   - username (String, Unique)
   - email (String, Unique)
   - password (Hashed String)
   - created_at (Timestamp)
   - is_admin (Boolean)

### Authentication Flow
2. Login through `/login/` endpoint 
4. Logout via `/logout/` endpoint to invalidate token

## Installation

### Docker Setup
Prerequisites:
- Docker
- Docker-compose

Commands:
```bash
docker build -t booking-system .
docker-compose up
```

### Python Setup
Prerequisites:
- Python 3.11
- PostgreSQL

Installation:
```bash
pip install -r requirements.txt
```

## Admin Access
Default credentials:
- Username: admin
- Password: admin

## API Documentation

### Resources
#### GET /resources/
Fetches all available resources.

Response:
```json
{
    "message": "Resources fetched successfully",
    "resources": [
        {
            "name": "string",
            "description": "string",
            "total_quantity": "integer",
            "available_quantity": "integer"
        }
    ],
    "out of stock resources": [
        {
            "name": "string",
            "description": "string",
            "total_quantity": "integer",
            "available_quantity": "integer"
        }
    ]
}
```

#### POST /resources/
Creates a new resource.

Request Body:
```json
{
    "name": "string",
    "description": "string",
    "total_quantity": "integer",
    "available_quantity": "integer"
}
```

### Bookings
#### GET /bookings/
Retrieves all bookings.

Response:
```json
[
    {
        "resource": "integer",
        "purchase_quantity": "integer",
        "booking_date": "datetime with timezone"
    }
]
```

#### POST /bookings/
Creates a new booking.

Request Body:
```json
{
    "resource": "String",
    "purchase_quantity": "integer"
}
```

### Users
#### GET /users/
Retrieves user information.

Response:
```json
[
    {
        "id": "integer",
        "username": "String",
        "email": "String"
    }
]
```

#### POST /users/
Creates a new user.

Request Body:
```json
{
    "username": "String",
    "email_address": "String",
    "password": "String",
    "confirm_password": "String"
}
```

### Authentication
#### POST /login/
Authenticates a user.

Request Body:
```json
{
    "username": "String",
    "password": "String"
}
```

#### POST /logout/
Logs out the current user.

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Data Flow
1. Client makes authenticated request to API
2. API validates request and permissions
3. Database operation is performed
4. Response is returned to client