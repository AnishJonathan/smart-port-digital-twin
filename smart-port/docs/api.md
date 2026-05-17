# API Documentation

This document outlines the internal routing structure of the Smart Port Platform. Since Phase 1 focuses on a server-rendered Jinja application, these are primarily UI endpoints rather than a RESTful JSON API.

## Authentication Routes

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/auth/login` | Renders the login page. Redirects to dashboard if already authenticated. | Public |
| POST | `/auth/login` | Processes the login credentials. On success, sets session cookie and redirects. | Public |
| GET | `/auth/logout` | Destroys the user session and redirects to the login page. | Authenticated |

## Dashboard Routes

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/dashboard/` | Renders the main dashboard index displaying statistics and charts. | Authenticated |

*(Future Phase: REST endpoints like `/api/v1/sensors` or `/api/v1/vessels` will be added here).*
