# Setup Documentation

This guide provides step-by-step instructions for getting the Smart Port Platform running on your local machine.

## Prerequisites
- Python 3.10+
- MySQL 8.0+ (Optional for local dev, highly recommended)
- Docker & Docker Compose (Optional but recommended for containerized testing)

## 1. Local Environment Setup

**Clone or navigate to the project directory:**
```bash
cd smart-port
```

**Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## 2. Configuration Setup

Copy the example environment file:
```bash
cp .env.example .env
```
Edit the `.env` file to match your desired settings. 

### Database Configuration
- **Primary:** The application defaults to MySQL if the `MYSQL_*` variables are provided and the host is reachable.
- **Fallback:** If MySQL is not reachable or the variables are missing, the `development` environment will automatically fall back to using SQLite (created in `instance/smartport_dev.sqlite`), allowing you to run the app instantly without setting up a DB server.

## 3. Running the Application (Local Dev)

Start the Flask development server:
```bash
flask run --host=0.0.0.0 --port=5000
```
On the first run, the database tables will be automatically created. 
A default Admin user will also be created with:
- **Email:** `admin@smartport.com`
- **Password:** `admin123`

## 4. Running via Docker (Production Simulation)

To spin up both the MySQL database and the Flask application (running on Gunicorn) using Docker:

```bash
docker-compose up --build -d
```
The application will be accessible at `http://localhost:8000`.
To stop the services:
```bash
docker-compose down
```
