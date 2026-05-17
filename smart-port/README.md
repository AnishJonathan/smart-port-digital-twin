# Smart Port Digital Twin Platform 🚢

A production-grade web application for monitoring and managing port operations. Built with a strong emphasis on backend architecture, scalability, and DevOps readiness.

## 🌟 Project Overview
This project represents Phase 1 of the Smart Port Digital Twin Platform, providing robust authentication and a minimal, functional dashboard for real-time statistics (e.g., Active Ships, Total Containers). It is designed to be easily extensible and deployment-ready for modern cloud infrastructure.

## 🏗️ Architecture

```
smart-port/
│
├── app.py                  # Application factory and entry point
├── config.py               # Environment-based configuration logic
├── requirements.txt        # Python dependencies
├── .env.example            # Template for environment variables
├── .gitignore              # Standard ignore file for Git
├── Dockerfile              # Multistage Docker build configuration
├── docker-compose.yml      # Local dev/test infrastructure setup
│
├── templates/              # Jinja templates (Bootstrap minimal UI)
│   ├── base.html           # Base layout
│   ├── auth/               # Login templates
│   └── dashboard/          # Dashboard layout
│
├── static/                 # Static assets (CSS/JS)
│
├── routes/                 # Flask Blueprints
│   ├── auth.py             # Authentication routing
│   └── dashboard.py        # Dashboard routing
│
├── models/                 # SQLAlchemy ORM Models
│   └── user.py             # User roles and auth methods
│
├── database/               # Database instance initialization
│
└── docs/                   # Comprehensive project documentation
```

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Flask-Blueprints, Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Database:** MySQL (Primary Production) with automatic SQLite fallback for local development. PyMySQL engine.
- **Frontend:** HTML, Bootstrap 5, Jinja Templates, Chart.js
- **DevOps:** Docker, Docker Compose, Gunicorn

## 🛣️ Future Roadmap
- **Phase 2 (IoT Integration):** Ingest real-time sensor data from cranes and port gates.
- **Phase 3 (Logistics API):** Expose REST/GraphQL APIs for external logistics companies.
- **Phase 4 (Kubernetes Deployment):** Helm charts and CI/CD pipelines (GitHub Actions/GitLab CI) to deploy to AWS EKS.

## 📚 Documentation
Please refer to the `docs/` folder for in-depth documentation:
- [Setup Guide](docs/setup.md)
- [Developer Architecture](docs/developer.md)
- [API Routes](docs/api.md)
