# Flask Users API

This is a simple, scalable RESTful API for user management built with Flask and MongoDB.

## Overview

Flask Users API provides a complete backend solution for user management with the following features:

- User creation with secure password hashing
- User retrieval
- User updates
- User deletion
- Input validation
- Error handling
- Rate limiting (30 requests per second)

## Technology Stack

- **Flask**: Lightweight web framework for Python
- **Flask-RESTful**: Extension for building REST APIs with Flask
- **Flask-Bcrypt**: Password hashing extension for secure authentication
- **Flask-Limiter**: Extension for rate limiting API endpoints
- **MongoDB**: NoSQL database for data storage
- **MongoEngine**: MongoDB ODM (Object Document Mapper) for Python
- **Docker**: Containerization platform
- **Docker Compose**: Tool for defining and running multi-container Docker applications

## API Endpoints

| Endpoint          | Method | Description                    |
| ----------------- | ------ | ------------------------------ |
| `/api/users`      | GET    | Retrieve all users             |
| `/api/users`      | POST   | Create a new user              |
| `/api/users/<id>` | GET    | Retrieve a specific user by ID |
| `/api/users/<id>` | PUT    | Update a specific user by ID   |
| `/api/users/<id>` | DELETE | Delete a specific user by ID   |

## Data Model

### User

```json
{
  "id": "string",
  "name": "string",
  "email": "string"
}
```

- `name`: Required, maximum 30 characters
- `email`: Required, must be unique and valid email format
- `password`: Required, minimum 8 characters (not returned in responses)

## Setup and Installation

### Development Setup

1. Clone the repository
   ```sh
   git clone https://github.com/HarshNarayanJha/flask_users
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables. Create a `.env` file. Check out `.env.example` for reference:

4. Run the application in development mode:
   ```sh
   python run.py
   ```

### Production Setup with Docker

1. Clone the repository
2. Make sure Docker and Docker Compose are installed on your system
3. Run the application using Docker Compose:
   ```sh
   docker compose up --build
   ```

This will start two services:

- **api**: The Flask application (exposed on port 5000)
- **db**: MongoDB database with persistent volume storage (exposed on default MongoDB port 27017)

The database data will be preserved in a volume, ensuring your data persists between container restarts.

After starting the containers, the API will be accessible at `http://localhost:5000`.

## Error Handling

The API provides detailed error responses for various scenarios:

- Validation errors
- Duplicate email addresses
- User not found
- Invalid input data
- Rate limit exceeded

## Security

- Passwords are hashed using bcrypt before storing in the database
- Sensitive user data (passwords) are never returned in API responses
- Rate limiting protects against brute force and DoS attacks (30 requests per second)

## Example Usage

I don't use Postman for API testing. I use [posting](https://github.com/darrenburns/posting) for API testing.

### Create a new user

```sh
POST /api/users
Content-Type: application/json

{
  "name": "Mario",
  "email": "mario@example.com",
  "password": "password123"
}
```

### Retrieve all users

```sh
GET /api/users
```

### Retrieve a specific user

```sh
GET /api/users/60d21b4667d0d8992e610c85
```

### Update a user

```sh
PUT /api/users/60d21b4667d0d8992e610c85
Content-Type: application/json

{
  "name": "Mario Mario"
}
```

### Delete a user

```sh
DELETE /api/users/60d21b4667d0d8992e610c85
```
