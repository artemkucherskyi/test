
# FastAPI Odoo Sync & API

This repository contains a FastAPI application that synchronizes contacts and invoices from an Odoo instance using XML-RPC and exposes a RESTful API to retrieve this data. The API is secured with JWT-based authentication. The application is containerized with Docker and is deployed to a DigitalOcean Droplet using a CI/CD pipeline built with GitHub Actions.

## Features

- **Odoo Synchronization:**  
  Synchronizes contacts (`res.partner`) and invoices (`account.move`) from an Odoo instance into a local database using SQLAlchemy.

- **RESTful API:**  
  Provides endpoints to retrieve contacts and invoices. Endpoints are secured with JWT authentication.

- **Dockerized Application:**  
  A Dockerfile is provided for building a containerized version of the application.

- **CI/CD with GitHub Actions:**  
  Automatically builds the Docker image and deploys it to a DigitalOcean Droplet via SSH (using an SSH password) when changes are pushed to the `main` branch.

## Project Structure

```
chift/
├── .env                     # Environment variable definitions (not committed)
├── Dockerfile               # Docker configuration for containerizing the app
├── main.py                  # FastAPI application
├── models.py                # SQLAlchemy models and database setup
├── sync_data.py             # Script to synchronize data from Odoo
├── requirements.txt         # Python dependencies
└── .github/
    └── workflows/
        └── ci.yml           # GitHub Actions CI/CD workflow configuration
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

For deployment on your DigitalOcean Droplet, store your `.env` file outside of your repository (for example, at `/home/youruser/app_env/.env`) and set the path as a secret in GitHub Actions.

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create a Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Synchronization Script (Optional)

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

## Deployment on DigitalOcean

This project is deployed to a DigitalOcean Droplet using Docker. Follow these steps:

1. **Prepare Your Droplet:**  
   - Create a Droplet (Ubuntu is recommended).  
   - Install Docker:

     ```bash
     sudo apt update
     sudo apt install -y docker.io
     sudo systemctl enable docker
     sudo systemctl start docker
     ```

2. **Secure Environment File:**  
   Create a secure environment file on your Droplet (e.g., `/home/youruser/app_env/.env`) with all the necessary environment variables.

3. **CI/CD via GitHub Actions:**  
   A GitHub Actions workflow is provided to build and deploy the Docker image to your Droplet via SSH (using an SSH password).

## GitHub Actions CI/CD

The workflow file is located at `.github/workflows/ci.yml` and performs the following actions:
- Checks out the code.
- Sets up Docker Buildx.
- Builds the Docker image.
- Saves the image to a tar file.
- Transfers the tar file to your DigitalOcean Droplet via SCP.
- Connects to your Droplet via SSH (using an SSH password) to load the image, stop the existing container (if any), and run the new container with the specified environment file.

### GitHub Secrets

Before the workflow can run, set the following secrets in your GitHub repository:

- **DO_HOST:** Your DigitalOcean Droplet’s public IP address.
- **DO_USER:** The SSH username for your Droplet.
- **DO_SSH_PASSWORD:** Your Droplet’s SSH password.
- **DO_ENV_PATH:** The path to your environment file on the Droplet (e.g., `/home/youruser/app_env/.env`).

## Testing

Tests are written using pytest. Run tests locally with:

```bash
pytest --maxfail=1 --disable-warnings -q
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For significant changes, open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Odoo External API Documentation](https://www.odoo.com/documentation/16.0/developer/reference/external_api.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [DigitalOcean](https://www.digitalocean.com/)
- [GitHub Actions](https://github.com/features/actions)
