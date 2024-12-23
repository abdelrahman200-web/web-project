# Customer Service for Hotel Room Management

This project is designed to streamline the process of managing hotel room registrations, check-ins, check-outs, and customer interactions using Python and SQL Server. It provides an efficient API interface for handling all aspects of room management and customer service.

## Features

1. **Room Management**:
   - Add new rooms with details such as room number, type, floor, capacity, price, and status.
   - Update room details and manage room availability.

2. **Customer Management**:
   - Add, search, and retrieve customer details.
   - Track customer registrations and interactions.

3. **Registration Management**:
   - Handle room check-ins and check-outs.
   - Track registration details, payment status, and customer notes.

4. **Request Management**:
   - Manage customer requests and update their status.

5. **Database Integration**:
   - SQL Server integration for secure and reliable data storage.

6. **API Routes**:
   - RESTful API design for seamless integration with frontend or third-party applications.

## Technologies Used

- **Backend**: Python (Flask for API development)
- **Database**: SQL Server
- **Frontend**: HTML/CSS (for user interfaces)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/hotel-room-management.git
   cd hotel-room-management
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Configuration**:
   - Create a SQL Server database and execute the SQL scripts provided in the `database/` folder to set up the required tables.
   - Update the `conn_str` variable in the Python scripts with your database connection details.

4. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`.

## API Endpoints

- **Room Management**:
  - `POST /add_room`: Add a new room.
  - `GET /rooms`: Fetch all rooms.

- **Customer Management**:
  - `POST /add_customer`: Add a new customer.
  - `GET /customers`: Fetch all customers.

- **Registration Management**:
  - `POST /check_in`: Check-in a customer.
  - `POST /check_out`: Check-out a customer.

- **Request Management**:
  - `POST /add_request`: Add a new request.
  - `PATCH /update_request_status`: Update the status of a request.

## Usage

- Use the provided API endpoints to integrate this system with your hotel management frontend or other systems.
- Customize the SQL queries and Python code as needed to fit specific requirements.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

For any inquiries or issues, feel free to open an issue on GitHub or contact the project maintainer.

---

### Notes

- Colors used in the project:
  - Primary: `#F5B813`
  - Secondary: `#FCC737`
- Ensure proper database setup before running the application.

Happy coding!
