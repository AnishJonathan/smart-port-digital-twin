# 🚢 Smart Port Digital Twin Platform

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Overview

The **Smart Port Digital Twin Platform** is a role-based logistics simulation system that replicates real-world port operations such as ship movement, container lifecycle tracking, crane monitoring, and congestion management.

It is designed as a **digital twin of a modern seaport**, combining simulation, analytics, and role-based control in a unified dashboard.

---

## 🌍 Real-World Problem

Modern ports suffer from:

- Congestion & inefficient vessel scheduling  
- Lack of real-time visibility into cargo flow  
- Poor coordination between operational roles  
- Equipment monitoring gaps (cranes, yard systems)  
- Limited predictive operational intelligence  

### ✔️ Solution Provided

This system solves these by introducing:

- Real-time **port operations dashboard**
- **Lifecycle tracking** of ships & containers
- **IoT-inspired crane monitoring system**
- Role-based operational control (RBAC)
- Simulation-driven congestion engine
- Audit logging for accountability

---

## 🏗️ System Architecture

```mermaid
graph TD
A[Frontend: Jinja2 + Bootstrap] --> B[Flask Application Layer]
B --> C[Business Logic Layer]
C --> D[Simulation Engine + RBAC + Services]
D --> E[SQLAlchemy ORM]
E --> F[MySQL Database]
B --> G[APScheduler Background Jobs]
