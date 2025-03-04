# quiz_master_23f2001161
This is a project for Modern Application Developement I

# Quiz Master Application

## Description

This is a Flask-based web application for managing quizzes, subjects, and chapters. It includes user authentication, role-based access control (admin), and database integration using SQLAlchemy.

## Features

*   User registration and login
*   Admin role with access to manage users, subjects, and chapters
*   Subject management (add, edit, delete)
*   Chapter management (add, edit, delete)

## Technologies Used

*   Python
*   Flask
*   Flask-Login
*   SQLAlchemy
*   HTML
*   CSS
*   Bootstrap

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required Python packages:**

    ```bash
    pip install Flask Flask-Login SQLAlchemy
    ```

3.  **Database Configuration:**

    *   The application uses a database (e.g., SQLite, PostgreSQL).
    *   Modify the `models/database_innit.py` file to configure the database connection string.

4.  **Run the Application:**

    ```bash
    python app.py
    ```

5.  **Access the application in your browser:**

    Open your web browser and go to `http://127.0.0.1:5000/`

## Usage

*   **Login:** Existing users can log in using their registered email and password.
*   **Registration:** New users can register an account.
*   **Admin Access:**
    *   Log in with an admin account.
    *   Navigate to `/admin/home` to access the admin panel.
    *   From the admin panel, you can manage users, subjects, and chapters.

## Database Structure

The application uses the following database tables:

*   `User`: Stores user information (full name, email, username, password, etc.).
*   `Subject`: Stores subject information (subject ID, name, description).
*   `Chapter`: Stores chapter information (chapter ID, subject ID, name, description).

## Important Notes

*   **Security:** This is a basic implementation and may have security vulnerabilities.  Implement proper security measures (e.g., password hashing, input validation) before deploying to a production environment.
*   **Error Handling:** The application includes basic error handling, but more robust error handling should be implemented.
*   **Templates:** HTML templates are located in the `templates` directory.
*   **Models:** Database models are defined in the `models` directory.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

