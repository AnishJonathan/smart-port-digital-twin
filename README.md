# 🚢 Smart Port Digital Twin Platform

A cloud-ready **Smart Port Digital Twin System** that simulates real-world port operations including ships, containers, cranes, congestion control, and IoT-driven analytics with role-based access control and real-time simulation engine.

---

# 🌍 Overview

The **Smart Port Digital Twin Platform** is an enterprise-grade simulation system designed to replicate real-world port operations.

It models:

* 🚢 Ship arrivals, docking, and departures
* 📦 Container lifecycle tracking
* 🏗️ Crane operations with simulated IoT telemetry
* 🌦️ Weather-aware congestion logic
* 📊 Real-time operational dashboards
* 🔐 Role-based access control (RBAC)
* 🧾 Audit logging for system transparency

This project demonstrates how modern ports can evolve into **data-driven, AI-assisted logistics ecosystems**.

---

# 🎯 Key Features

## 🧠 Digital Twin Simulation Engine

* Real-time simulation of port activity (every 10 seconds)
* Rule-based congestion control system
* Weather-driven operational adjustments
* Autonomous ship/container lifecycle progression

## 🚢 Port Operations Management

* Ship registration, tracking, and lifecycle management
* Container tracking from arrival → delivery
* Crane monitoring with simulated IoT metrics

## 🔐 Enterprise RBAC System

* Admin → Full system control
* Port Manager → Operational management
* Logistics Officer → Workflow-level access
* Strict backend + UI enforcement

## 📊 Live Dashboard

* Real-time KPI monitoring
* Port congestion indicator (Low / Medium / High)
* System health status (DB, simulation engine, weather API)
* Activity feed (audit logs)

## 🧾 Audit Logging System

* Tracks all system actions:

  * Ship creation/deletion
  * Container updates
  * Status transitions
  * Simulation events

## 🐳 Containerized Architecture

* Fully Dockerized system
* Multi-container setup:

  * Flask Application
  * MySQL Database
* Production-ready configuration

---

# 🏗️ System Architecture

```
                ┌────────────────────────────┐
                │      Frontend (Jinja2 UI)   │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │   Flask Backend (API Layer) │
                └────────────┬───────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌──────────────┐   ┌────────────────┐   ┌─────────────────┐
│ MySQL DB     │   │ Simulation     │   │ Weather Service │
│ (Persistent) │   │ Engine (APS)   │   │ API/Fallback    │
└──────────────┘   └────────────────┘   └─────────────────┘
                             │
                             ▼
                 ┌────────────────────────┐
                 │ Audit & Logging Layer  │
                 └────────────────────────┘
```

---

# 🧱 Tech Stack

### Backend

* Flask (Python)
* SQLAlchemy ORM
* Flask-Login (Authentication)
* APScheduler (Simulation Engine)

### Database

* MySQL 8.0

### Frontend

* HTML5 / CSS3
* Bootstrap 5
* Chart.js (Analytics)
* Jinja2 templating

### DevOps

* Docker
* Docker Compose
* Gunicorn (Production WSGI server)

---

# 🧩 Database Schema

## Users

```
id | name | email | password_hash | role | created_at
```

## Ships

```
id | name | status | destination | fuel_level | arrival_time
```

## Containers

```
id | container_id | location | status | priority | ship_id
```

## Cranes

```
id | crane_name | status | temperature | load_capacity | health
```

## Audit Logs

```
id | user | action | target | timestamp
```

---

# 🔄 Simulation Engine

The system includes an autonomous simulation engine:

* Runs every **10 seconds**
* Updates:

  * Ship statuses
  * Container movement
  * Crane load & temperature
  * Congestion level

### Example Logic:

* High ship density → Increased congestion
* Crane overload → Risk state
* Weather impact → Delays

---

# 🔐 Role-Based Access Control

| Role              | Permissions                |
| ----------------- | -------------------------- |
| Admin             | Full CRUD + system control |
| Port Manager      | Operational updates        |
| Logistics Officer | Workflow tracking only     |

---

# 🐳 Running the Project (Docker)

## 1. Clone Repository

```bash
git clone https://github.com/your-username/smart-port.git
cd smart-port
```

## 2. Start Services

```bash
docker compose up --build
```

## 3. Access Application

```
http://localhost:8000
```

---

# 🧪 Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

---

# 📸 Screenshots

> Add your UI screenshots here

```
Dashboard View
Ship Management
Container Tracking
Crane Monitoring
Audit Logs
```

---

# 🚀 DevOps Highlights

* Dockerized microservice-style architecture
* Persistent MySQL volume storage
* Production-grade Gunicorn deployment
* Environment-based configuration
* Logging + health monitoring readiness

---

# 📈 Real-World Problem It Solves

Modern ports face:

* Inefficient cargo tracking
* Lack of real-time visibility
* Poor resource allocation
* Delayed decision-making

This system simulates a solution for:

> “Digitally monitoring and optimizing port operations using real-time data and intelligent simulation.”

---

# 🧠 Future Enhancements

* 🔌 Real IoT integration (MQTT / Raspberry Pi sensors)
* 📡 WebSocket-based real-time dashboard updates
* 🤖 ML-based delay prediction
* ☁️ Cloud deployment (AWS / Kubernetes)
* 📊 Advanced analytics dashboard

---

# 👨‍💻 Author

**Anish Jonathan**
B.Tech CSE | MSc Software Engineering (Sweden Dual Degree)

---

# ⭐ If you like this project

Give it a star ⭐ and follow for more system-level engineering projects.

---

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---


