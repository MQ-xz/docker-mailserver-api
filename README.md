# docker-mailserver-api

Just a clone of [docker-mailserver](https://github.com/docker-mailserver/docker-mailserver) with a REST API interface. so you can manage your mail CRUD operations via REST API.
This project is a simple REST API for managing email accounts using Docker Mailserver. It provides endpoints to create, update, and delete email accounts.

# API Documentation

BASE URL: `http://178.18.254.224:8983`

## User Mail Management

### Endpoint: `/user_mails`

#### POST `/user_mails`

Create a new email account.

**Headers:**

- `Authorization`: API key (required)

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

- **201 Created**
  ```json
  {
    "message": "Mail created successfully"
  }
  ```
- **400 Bad Request**
  ```json
  {
    "error": "Invalid request data"
  }
  ```
- **401 Unauthorized**
  ```json
  {
    "error": "Invalid API key"
  }
  ```
- **500 Internal Server Error**
  ```json
  {
    "error": "Failed to create mail"
  }
  ```

---

#### PATCH `/user_mails`

Update the password for an existing email account.

**Headers:**

- `Authorization`: API key (required)

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "newsecurepassword"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "message": "Mail updated successfully"
  }
  ```
- **400 Bad Request**
  ```json
  {
    "error": "Invalid request data"
  }
  ```
- **401 Unauthorized**
  ```json
  {
    "error": "Invalid API key"
  }
  ```
- **500 Internal Server Error**
  ```json
  {
    "error": "Failed to update mail"
  }
  ```

---

#### DELETE `/user_mails`

Delete an existing email account.

**Headers:**

- `Authorization`: API key (required)

**Request Body:**

```json
{
  "email": "user@example.com"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "message": "Mail deleted successfully"
  }
  ```
- **400 Bad Request**
  ```json
  {
    "error": "Invalid request data"
  }
  ```
- **401 Unauthorized**
  ```json
  {
    "error": "Invalid API key"
  }
  ```
- **500 Internal Server Error**
  ```json
  {
    "error": "Failed to delete mail"
  }
  ```
