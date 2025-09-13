# Real-Time Polling Application API

This project implements a real-time polling application backend using FastAPI, SQLAlchemy, MySQL, and WebSockets.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd real-time-polling-app
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup:**
    *   Ensure you have a MySQL server running.
    *   Create a database for the application (e.g., `polling_app_db`).
    *   Set the `DATABASE_URL` environment variable with your MySQL connection string. Example:
        ```
        export DATABASE_URL="mysql+mysqlconnector://user:password@host:port/polling_app_db"
        ```
        (Replace `user`, `password`, `host`, `port`, and `polling_app_db` with your MySQL credentials and database name.)

5.  **Run Database Migrations (if applicable, or create tables directly):**
    *   For this project, tables will be created on application startup if they don't exist.

6.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

7.  **Access the API documentation:**
    Once the server is running, open your browser to `http://127.0.0.1:8000/docs` for the OpenAPI (Swagger UI) documentation.

## API Endpoints

(To be filled in as endpoints are implemented)

## WebSocket Endpoints

(To be filled in as WebSocket endpoints are implemented)

## Technologies Used

*   **Backend Framework:** FastAPI (Python)
*   **Database:** MySQL
*   **ORM:** SQLAlchemy
*   **Real-time Communication:** WebSockets
