# AWS EC2 Production Deployment Guide

This guide outlines the architecture and deployment strategy for migrating the Smart Port Digital Twin Platform to a production AWS EC2 environment.

## 1. Target Architecture
- **Compute:** AWS EC2 Instance (t3.micro or t3.small for Phase 1).
- **OS:** Ubuntu 22.04 LTS.
- **Web Server / Reverse Proxy:** Nginx (Handles SSL termination and static file serving).
- **Application Server:** Gunicorn running the Flask app inside Docker, or managed by systemd.
- **Database:** AWS RDS (MySQL) is highly recommended for production data safety rather than a Dockerized database on the EC2 instance.

## 2. Server Provisioning Steps
1. Spin up an EC2 instance and assign an Elastic IP.
2. Open Security Group ports: 
   - `22` (SSH)
   - `80` (HTTP)
   - `443` (HTTPS)
3. SSH into the instance:
   ```bash
   ssh -i your-key.pem ubuntu@<ec2-ip-address>
   ```

## 3. Environment Setup on EC2
Install Docker and Docker Compose:
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
```

Clone the repository and set up the production environment variables:
```bash
git clone https://github.com/your-repo/smart-port.git
cd smart-port
cp .env.example .env
nano .env # Insert production RDS credentials and a strong SECRET_KEY
```

## 4. Deploying with Docker Compose
To utilize the exact environment tested in CI, you can simply run:
```bash
docker-compose up --build -d
```
*Note: In a true production environment with RDS, you would remove the `db` service from `docker-compose.yml` and only spin up the `app` service pointing to the RDS endpoint.*

## 5. Reverse Proxy & SSL (Nginx + Certbot)
To expose the application to the internet securely:

1. Install Nginx:
   ```bash
   sudo apt install nginx -y
   ```
2. Create an Nginx configuration file (`/etc/nginx/sites-available/smartport`):
   ```nginx
   server {
       listen 80;
       server_name port.yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. Enable the site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/smartport /etc/nginx/sites-enabled
   sudo systemctl restart nginx
   ```
4. Obtain an SSL Certificate using Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d port.yourdomain.com
   ```

## 6. Continuous Deployment
For future iterations, configure GitHub Actions to SSH into the EC2 instance automatically, pull the latest code on the `main` branch, and run `docker-compose up --build -d` ensuring zero-downtime deployments.
