# Phase 1 Manual Testing Checklist

Before cutting a release or moving to Phase 2, ensure all the following manual tests pass locally. This acts as our QA procedure.

## 1. Authentication Flow
- [ ] **Valid Login:** Navigate to `/auth/login`. Enter `admin@smartport.com` and `admin123`. Verify successful redirect to the Dashboard.
- [ ] **Invalid Login:** Enter incorrect credentials. Verify a Bootstrap alert appears stating "Please check your login details and try again."
- [ ] **Route Protection:** Open an incognito window and attempt to visit `/dashboard/`. Verify you are automatically redirected back to `/auth/login`.
- [ ] **Logout:** From the Dashboard, click Logout. Verify redirect to login page and session termination.
- [ ] **Remember Me:** Check the "Remember me" box during login. Close the browser entirely, reopen it, and navigate to `/dashboard/`. Verify the session persists.

## 2. Dashboard UI & Data
- [ ] **Responsiveness:** Shrink the browser window to mobile size. Verify the navbar collapses correctly and statistics cards stack vertically.
- [ ] **Data Injection:** Verify that the 4 statistic cards (Active Ships, Total Containers, etc.) have data populated and are not empty or throwing Jinja template errors.
- [ ] **Chart Rendering:** Ensure the `Chart.js` bar chart renders in the "Weekly Container Throughput" section and tooltips appear when hovering over the bars.

## 3. DevOps & Health Infrastructure
- [ ] **Health Endpoint:** Send a GET request to `http://localhost:8000/health`. Verify it returns a 200 OK with `{"status": "healthy", "database": "connected"}`.
- [ ] **Logs Output:** Observe the terminal running the application. Verify logs are outputting in a structured JSON format containing timestamps, levels, and modules.
- [ ] **Local Fallback DB:** Delete the `.env` file (or temporarily rename it), start the Flask app natively (`flask run`), and verify it automatically creates and utilizes `instance/smartport_dev.sqlite` with a warning message in the console.
