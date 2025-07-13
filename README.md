# Pet Recommendation System

A FastAPI application for managing pets with CRUD operations using AWS DynamoDB.
It is part of a bigger project with microservice architecture. Other parts coming soon.

This project aims at enhancing user experience when they are looking to adopt a pet from a shelter. It encourages future pet owners to be more responsible and make a reasonable choice by providing an advanced search tool based on their preferences and budget, as well as recommends similar pets for adoption with a slight shift from initial preferences.


### Pet Management
- `POST /pets` - Create a new pet
- `PUT /pets/{pet_id}` - Update a pet
- `DELETE /pets/{pet_id}` - Delete a pet


### Utility
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)

## Pet Model

```json
{
  "id": "string (auto-generated UUID)",
  "name": "string",
  "species": "string",
  "age": "integer (>= 0)",
  "temperament": "string",
  "health": "string",
  "sociability": "string",
  "budget": "float (> 0.0)"
}
```

## Setup and Installation

### Prerequisites

- Python 3.13+
- AWS Account with DynamoDB access

### 1. Clone and Install Dependencies

```bash
# Install dependencies
uv sync
```

### 2. Configure Environment Variables

Copy the environment template and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# DynamoDB Configuration
DYNAMODB_TABLE_NAME=pets
AWS_REGION=us-east-1

# Server Configuration
HOST=0.0.0.0
PORT=8000

# use IAM roles for AWS in production. I will not be using AWS credentials in this source code, even for local development.

```


### 4. Run the Application

```bash
# Using Python directly
python main.py

# Or using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Development and deployment plan
The other microservices are in development. This microservice is built to be an internal part of a bigger system, therefore the security is provided by higher-level tools like authentication on API gateway level + VPC + security groups. IAM is going to be used for access management.
