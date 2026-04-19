# Calculator API

FastAPI backend for **user registration/login** and **calculation CRUD (BREAD)** operations, with **integration tests**, **OpenAPI documentation**, and **CI/CD** configured to build and push a Docker image to Docker Hub.

## Assignment Coverage

This project satisfies the following assignment requirements:

- `POST /users/register`
- `POST /users/login`
- `GET /calculations`
- `GET /calculations/{calculation_id}`
- `POST /calculations`
- `PUT /calculations/{calculation_id}`
- `PATCH /calculations/{calculation_id}`
- `DELETE /calculations/{calculation_id}`
- Pydantic validation for requests and responses
- Secure password hashing
- Integration tests with `pytest`
- GitHub Actions workflow for automated testing
- Docker image build and push to Docker Hub

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- pytest
- Docker
- GitHub Actions

## Project Structure

```text
app/
  auth.py
  database.py
  main.py
  models.py
  schemas.py
  routers/
    __init__.py
    users.py
    calculations.py
tests/
  conftest.py
  test_users.py
  test_calculations.py
.github/workflows/
  ci.yml
Dockerfile
requirements.txt
README.md
reflection.md
```

## Features

### User Endpoints

- Register a new user
- Login with email and password
- Passwords are stored as hashed values

### Calculation Endpoints

- Browse all calculations
- Read one calculation by ID
- Add a new calculation
- Update a calculation with `PUT` or `PATCH`
- Delete a calculation

## Prerequisites

Install the following before running the project:

- Python 3.12+ or compatible version
- PostgreSQL
- Git
- Docker Desktop (for Docker testing)

## Install Dependencies

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables

This project uses PostgreSQL through `DATABASE_URL` and `TEST_DATABASE_URL`.

### Main app database

#### Windows PowerShell

```powershell
$env:DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/calculator_db"
```

#### macOS / Linux

```bash
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/calculator_db
```

### Test database

#### Windows PowerShell

```powershell
$env:TEST_DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/calculator_test"
```

#### macOS / Linux

```bash
export TEST_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/calculator_test
```

> Update the username, password, host, and database names if your local PostgreSQL setup is different.

## Create Local Databases

Create two PostgreSQL databases:

- `calculator_db`
- `calculator_test`

Example using `psql`:

```sql
CREATE DATABASE calculator_db;
CREATE DATABASE calculator_test;
```

## Run the Application Locally

Start the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Once the server starts, open:

- App root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Manual API Checks via OpenAPI

Use `/docs` to manually verify the endpoints.

### 1. Register a user

`POST /users/register`

Sample request body:

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "supersecure123"
}
```

Expected result:

- Status code: `201 Created`
- Returns user ID, username, and email

### 2. Login

`POST /users/login`

Sample request body:

```json
{
  "email": "testuser@example.com",
  "password": "supersecure123"
}
```

Expected result:

- Status code: `200 OK`
- Message: `Login successful`

### 3. Create a calculation

`POST /calculations`

Sample request body:

```json
{
  "expression": "2 + 2",
  "result": 4
}
```

Expected result:

- Status code: `201 Created`
- Returns the created calculation with ID

### 4. Browse calculations

`GET /calculations`

Expected result:

- Status code: `200 OK`
- Returns a list of calculations

### 5. Read one calculation

`GET /calculations/{calculation_id}`

Expected result:

- Status code: `200 OK`
- Returns the selected calculation

### 6. Update a calculation

`PUT /calculations/{calculation_id}` or `PATCH /calculations/{calculation_id}`

Sample request body:

```json
{
  "expression": "3 + 4",
  "result": 7
}
```

Expected result:

- Status code: `200 OK`
- Returns the updated calculation

### 7. Delete a calculation

`DELETE /calculations/{calculation_id}`

Expected result:

- Status code: `204 No Content`

### 8. Validation and error checks

Also verify these cases in `/docs`:

- duplicate email registration returns `400`
- duplicate username returns `400`
- wrong login password returns `401`
- missing calculation fields return `422`
- invalid calculation ID returns `404`

## Run Integration Tests

Before running tests, point both variables to the test database.

### Windows PowerShell

```powershell
$env:DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/calculator_test"
$env:TEST_DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/calculator_test"
python -m pytest -v
```

### macOS / Linux

```bash
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/calculator_test
export TEST_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/calculator_test
python -m pytest -v
```

Expected result:

- all tests pass
- user tests pass
- calculation tests pass

## Docker

This assignment requires a Docker image that can be pushed to Docker Hub.

### Build the Docker image

```bash
docker build -t calculator-api .
```

### Run the Docker image

If PostgreSQL is running on your machine, pass a valid database URL when starting the container.

```bash
docker run -p 8000:8000 -e DATABASE_URL=postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/calculator_db calculator-api
```

Then open:

- `http://127.0.0.1:8000/docs`

## GitHub Actions CI/CD

The workflow file is:

```text
.github/workflows/ci.yml
```

The workflow:

1. starts a PostgreSQL service
2. installs dependencies
3. runs integration tests
4. builds the Docker image
5. pushes the image to Docker Hub after successful tests

### Required GitHub Secrets

Add these repository secrets in GitHub:

- `DOCKER_USERNAME`
- `DOCKERHUB_TOKEN`

## GitHub Repository Link

Replace this placeholder with your actual repository URL:

```text
https://github.com/<your-username>/<your-repository-name>
```

## Docker Hub Repository Link

Replace this placeholder with your actual Docker Hub repository URL:

```text
https://hub.docker.com/r/<your-dockerhub-username>/<your-image-name>
```

## Suggested Submission Screenshots

Take and submit screenshots of:

- successful GitHub Actions workflow run
- Swagger UI showing the endpoints
- application running in the browser
- successful endpoint execution in `/docs`
- terminal showing passing `pytest` results

## Reflection Document

Include a `reflection.md` file in the repository describing:

- what you built
- challenges you faced
- what you learned
- what you would improve next

## Troubleshooting

### `argon2` not installed

If you see an error related to Argon2 or `pwdlib`, install:

```bash
pip install "pwdlib[argon2]"
```

### Database connection errors

Make sure:

- PostgreSQL is running
- `DATABASE_URL` is correct
- `TEST_DATABASE_URL` is correct
- the databases exist

### Tests fail because tables already exist or old data exists

Use the test database only for test runs.

## Author Notes

Before submitting, update this README with:

- your actual GitHub repo link
- your actual Docker Hub link
- any project-specific setup differences from your machine
