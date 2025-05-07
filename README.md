# CS 5330: Social Media Analysis Database System

This project is for CS 5330. It is a full-stack web application for managing a database of an app that analyzes social media content through structured experiments. Users, posts, projects, fields, and analysis results are stored in a MySQL database, and exposed through a Flask REST API.

## 📁 Project Structure

```
backend/
├── app.py                  # Flask backend
├── config.py               # DB credentials
├── create_tables.sql       # SQL script for DB setup
├── tests/                  # Pytest unit and integration tests
└── requirements.txt        # Python dependencies

frontend/
├── [React app files]  # React frontend code
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or 3.12
- MySQL Server
- Node.js + npm (for frontend)
- Git (optional)

---

## ⚙️ Backend Setup

1. **Clone the repo and navigate to backend folder**
   ```bash
   git clone https://github.com/your-username/DBProject.git
   cd DBProject/backend
   ```

2. **Set up and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   source .venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If encountering errors on Mac:
   ```bash
   brew install pkg-config
   brew install mysql
   pip install -r requirements.txt
   ```

4. **Set up your MySQL DB**
   - Make sure MySQL is running.
   - Create a database titled db_project:

      ```bash
      mysql -u root -p -e "CREATE DATABASE db_project;"
      ```
   - Add connection settings in `config.py`:

     ```python
     MYSQL_HOST = 'localhost'
     MYSQL_USER = 'your_user'
     MYSQL_PASSWORD = 'your_password'
     MYSQL_DB = 'db_project'
     ```
   - Create a user (if 'your_user' is not root) and assign permissions:

      ```bash
      mysql -u root -p -e "CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password'; GRANT ALL PRIVILEGES ON db_project.* TO 'your_user'@'localhost'; FLUSH PRIVILEGES;"
      ```
   - Create tables by running `create_tables.sql` in backend:
   
      ```bash
      mysql -u your_user -p db_project < create_tables.sql
      ```

5. **Run Flask app**
   ```bash
   python app.py
   ```

   - Access at: `http://localhost:5050/`

---

## 💻 Frontend Setup

1. **Create new terminal and navigate to frontend folder**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start React app**
   ```bash
   npm start
   ```

   - Access at: `http://localhost:3000/`

---

## ✅ Running Tests

1. **Create new terminal and navigate to backend folder**
   ```bash
   cd backend
   ```

2. **Activate virtual environment (if not already)**
   ```bash
   .venv\Scripts\activate   # On Windows
   source .venv/bin/activate  # On Mac/Linux
   ```

3. **Run tests**
   ```bash
   pytest
   ```

---

## 🔗 API Overview

| Endpoint                      | Method | Description                               |
|------------------------------|--------|-------------------------------------------|
| `/add-user`                  | POST   | Add a new user                            |
| `/add-post`                  | POST   | Add a new post                            |
| `/add-project`               | POST   | Add a new research project                |
| `/add-analysisresult`        | POST   | Link post to a project's field/value      |
| `/query/experiment-results`  | GET    | Get results for a given project           |
| ...                          | ...    | [Many more available in `app.py`]         |

---

## 🛠 Example Workflow

1. Add a social media platform → `/add-socialmedia`
2. Add a user on that platform → `/add-user`
3. Add a post by that user → `/add-post`
4. Add an institute → `/add-institute`
5. Add a project under the institute → `/add-project`
6. Add fields to the project → `/add-field`
7. Add analysis results linked to a post → `/add-analysisresult`
8. Query posts by:
   - Social media → `/query/posts-by-media`
   - Period of time → `/query/posts-by-time`
   - Username of a certain media → `/query/posts-by-username`
   - First/last name → `/query/posts-by-name`
8. Query results by project → `/query/experiment-results`
