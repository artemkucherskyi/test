# FastAPI Odoo Sync & API

## API demo
API and swagger here:  
[http://164.92.234.94:8000/docs](http://164.92.234.94:8000/docs).

User - `admin`  
Password - `secret`

## Features

- **Odoo Synchronization:**  
  Synchronizes contacts (`res.partner`) and invoices (`account.move`) from an Odoo instance into a local database (used SQLite for simplicity).

- **RESTful API:**  
  Provides endpoints to retrieve contacts and invoices. Endpoints are secured with JWT authentication.

- **Dockerized Application:**  
  A Dockerfile is provided for building a containerized version of the application.

## Project Structure

```
repo/
├── .env_example             # Env file example
├── Dockerfile               # Docker configuration for containerizing the app
├── main.py                  # FastAPI application
├── models.py                # SQLAlchemy models and database setup
├── sync_data.py             # Script to synchronize data from Odoo
├── requirements.txt         # Python dependencies
├── tests/
│   ├── conftest.py          # Pytest configuration
│   ├── test_main.py         # Simple API tests
│   └── test_sync.py         # Simple sync tests
```

## Environment Variables

The application requires several environment variables to run. Create a `.env` file locally (this file should **not** be committed to your repository) with content similar to:

```env
# Odoo configuration
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your_odoo_db
ODOO_USERNAME=your_username_or_email
ODOO_PASSWORD=your_password

# Database configuration (default: SQLite)
DATABASE_URL=sqlite:///./local_data.db

# JWT configuration
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin credentials for API login
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secret
```

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/artemkucherskyi/test.git
cd test
```

### 2. Create a Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Synchronization Script

To fetch and synchronize data from Odoo, run:

```bash
python sync_data.py
```

### 4. Run the FastAPI Application Locally

```bash
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Docker

### Building the Docker Image

Build the Docker image with:

```bash
docker build -t my-fastapi-app .
```

### Running the Docker Container

Run the container locally:

```bash
docker run -d -p 8000:8000 --name fastapi-container my-fastapi-app
```

Your app will be available at [http://localhost:8000](http://localhost:8000).

## Testing

Tests have been added using pytest. To run the tests:

```bash
pytest --maxfail=1 --disable-warnings -q
```

## Cron Job Setup

To keep your local database synchronized with Odoo, you can schedule the `sync_data.py` script to run every 10 minutes using cron.

1. **Open your crontab editor:**

   ```bash
   crontab -e
   ```

2. **Add the following line to schedule the job every 10 minutes:**

   ```cron
   */10 * * * * /path/to/venv/bin/python /path/to/your/project/sync_data.py >> /path/to/your/project/sync.log 2>&1
   ```

   Replace `/path/to/venv/bin/python` with the path to your Python executable, and `/path/to/your/project/` with the directory where your project is located.

3. **Save and Exit:**  
   Your cron job is now scheduled to run every 10 minutes, and its output (including errors) will be appended to `sync.log`.
