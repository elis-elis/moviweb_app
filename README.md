# MoviWeb

### **Application Structure:**

1. **User Interface (UI):**
    - Built with **Flask**, **HTML**, and **CSS**.
    - Provides an interactive web interface for users to:
        - Select their identity from a list of users.
        - Manage their list of movies (add, delete, update, view).
2. **Data Management:**
    - A dedicated Python class will handle the data operations.
    - Functions needed:
        - Retrieve all users.
        - Retrieve movies for a specific user.
        - Update movies for a specific user.
3. **Database File:**
    - A file (likely `.db` or `.sqlite`) to store user and movie data.
    - Acts as the backend data source, accessible by the Python class for CRUD (Create, Read, Update, Delete) operations.

### **Core Functionalities:**

1. **User Selection:**
    - A feature allowing users to select their identity from a list of users (stored in the database).
2. **Movie Management:**
    - **Add a movie:** Users can enter movie details (name, director, year, rating).
    - **Delete a movie:** Users can remove a movie from their list.
    - **Update a movie:** Users can modify existing movie details.
    - **List all movies:** Users can view all movies on their list.
3. **Data Source Management:**
    - The Python class will handle all interactions with the database (like querying, updating, etc.).
