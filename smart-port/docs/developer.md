# Developer & Architecture Documentation

## Why this Architecture?

### 1. Application Factory Pattern (`app.py`)
The Application Factory pattern (`create_app`) allows for cleaner dependency injection and much easier testing. By not declaring a global `app` object directly in the root namespace, we can dynamically spawn testing instances of the application or configure it differently for various environments on the fly.

### 2. Flask Blueprints (`routes/`)
Using Blueprints isolates different domains of the application (`auth` vs. `dashboard`). This modular approach ensures that as the codebase scales (e.g., adding `billing` or `sensor_ingestion`), developers can work in isolated files without creating merge conflicts in a massive monolithic `routes.py` file.

### 3. Environment-Based Configuration (`config.py` & `.env`)
A fundamental DevOps best practice (12-Factor App methodology) is keeping configuration separate from code. 
- Using `config.py` alongside `.env` means we never hardcode secrets in source control. 
- The application implements a highly robust database strategy: it attempts to connect to MySQL (Primary), and if unavailable during a Development run, automatically falls back to an SQLite file. This drastically lowers the barrier to entry for local development while strictly enforcing MySQL in Production.

### 4. Authentication Choice (Flask-Login)
For Phase 1, the requirement dictates a server-rendered Jinja interface. Flask-Login natively leverages secure, HTTP-only session cookies that are automatically handled by the browser. 
- JWTs are designed for decoupled stateless environments (SPAs, Mobile Apps). Using JWTs with Jinja would require messy JavaScript injection of the token into HTTP Headers. 
- Flask-Login ensures state-of-the-art security for standard web platforms.

### 5. UI/UX Strategy
Bootstrap 5 is used to ensure the UI is clean, functional, and responsive, with zero custom CSS technical debt. The emphasis remains firmly on backend reliability and DevOps preparedness.
