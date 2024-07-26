
---

# Library Management System

## Project Description
This project describes the models and overall system design of a library management system app. Users can search for sections and books, while admins can manage books and sections.

## Technologies Used
- **Languages and Frameworks:** Python, HTML, Vue.js, Bootstrap, Flask, Flask-Login, Role Based Login, Flask-SQLAlchemy, Chart.js, SQLite, Celery, Redis
- **Core Programming Language:** Python
- **Main Frameworks:** Vue and Flask
- **User Management:** Flask-Login, Role Based Login
- **Database:** Flask-SQLAlchemy (SQL toolkit for SQLite)

## Features
- **Admin Management:** Manage sections, books, and users.
- **Section Management:** Create, edit, and delete sections; view and search books.
- **Book Management:** Create, edit, and delete books; filter books by name; revoke user access.
- **Insights / Summary:** View number of books in each section via bar graphs.
- **Search for Books / Section:** Filter by section and search by title, author, or content.
- **Book Return and Feedback:** Rent books with a 7-day return policy and provide feedback.
- **Reminders:** Daily, weekly, and monthly reminders for users; weekly reports for admin.

## Running the Project

### Prerequisites
- Python 3.8+
- Node.js and npm
- SQLite

### Backend Setup
1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the SQLite database:
    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Run the Flask app:
    ```sh
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run
    ```

### Frontend Setup
1. Navigate to the frontend directory:
    ```sh
    cd frontend
    ```

2. Install dependencies:
    ```sh
    npm install
    ```

3. Run the Vue.js app:
    ```sh
    npm run serve
    ```

### Running Celery
1. Start the Celery worker:
    ```sh
    celery -A app.celery worker --loglevel=info
    ```

### Accessing the Application
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:8080`

### Additional Notes
- Ensure Redis is running before starting Celery.
- Configuration settings can be modified in `config.py`.

---
