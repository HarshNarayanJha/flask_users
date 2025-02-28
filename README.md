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

## Technology Stack

- **Flask**: Lightweight web framework for Python
- **Flask-RESTful**: Extension for building REST APIs with Flask
- **Flask-Bcrypt**: Password hashing extension for secure authentication
- **MongoDB**: NoSQL database for data storage
- **MongoEngine**: MongoDB ODM (Object Document Mapper) for Python

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

1. Clone the repository
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables. Create a `.env` file with `MONGODB_URI`:

   ```sh
   MONGODB_URL="mongodb://localhost:PORT"
   ```

4. Run the application:
   ```sh
   flask run
   ```

## Error Handling

The API provides detailed error responses for various scenarios:

- Validation errors
- Duplicate email addresses
- User not found
- Invalid input data

## Security

- Passwords are hashed using bcrypt before storing in the database
- Sensitive user data (passwords) are never returned in API responses

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
