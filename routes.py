from flask import Flask , jsonify , Blueprint, request
import models
bp=Blueprint("route",__name__)
# Route to add a new registration
# Returns Else statement response
@bp.route('/register', methods=['POST'])
def register_customer():
    try:
        data = request.json  # Get data from request body
        if(models.add_registration(
            Id=data['Id'],
            CheckInDate=data['CheckInDate'],
            CheckOutDate=data['CheckOutDate'],
            TotalAmount=data['TotalAmount'],
            PaidAmount=data['PaidAmount'],
            RemainingAmount=data['RemainingAmount'],
            StayDuration=data['StayDuration'],
            accommodation=data['accommodation'],
            note=data['note'],
            customer=data['customer'],
            RoomNo=data['RoomNo'],
            status='check in'
        )):
         return jsonify({"message": "Registration added successfully."}), 201
        else:
               return jsonify({"error": str(e)}), 400   
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to delete a room by RoomNo
@bp.route('/rooms/<int:room_no>', methods=['DELETE'])
def delete_room(room_no):
    try:
        models.delate_Room(room_no)  # Call delate_Room function from models
        return jsonify({"message": "Room deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# route to return the data for dashboard
#No Problem
@bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    try:
        Ready_room, Room_count, registration_number, Requests_number, Complaints_number = models.dashbord()
        response = {
            "Ready_room": Ready_room,
            "Room_count": Room_count,
            "registration_number": registration_number,
            "Requests_number": Requests_number,
            "Complaints_number": Complaints_number
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get customers who are checked in
# Returns [] empty 
@bp.route('/customers/checkin', methods=['GET'])
def get_customers_check_in():
    try:
        customers_check_in = models.show_customer_check_in()  # Call show_customer_check_in from models
        return jsonify([dict(row) for row in customers_check_in]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get customers who have checked out
# Returns [] empty 
@bp.route('/customers/checkout', methods=['GET'])
def get_customers_check_out():
    try:
        customers_check_out = models.show_customer_check_out()  # Call show_customer_check_out from models
        return jsonify([dict(row) for row in customers_check_out]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route to handle room addition
@bp.route('/add-room', methods=['POST'])
def add_room_route():
    data = request.json 
    try:
        Room_number = data['Room_number']
        Roomtype = data['Roomtype']
        floorNumber = data['floorNumber']
        max = data['max']
        price = data['price']
        F = data['F']   #floor
        status = data['status']        
        message, status_code = models.add_Room(Room_number, Roomtype, floorNumber, max, price, F, status)
        return jsonify({"message": message}), status_code
    
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {str(e)}"}), 400 
    
  # Route to handle update-room
  # Working
@bp.route('/update-room', methods=['POST'])
def update_room_route():
    data = request.json  # Get data from request body
    try:
        Room_number = data['Room_number']
        Roomtype = data['Roomtype']
        floorNumber = data['floorNumber']
        max_capacity = data['max_capacity']
        price = data['price']
        F = data['F']
        status = data['status']
        
        result = models.update_room_info(Room_number, Roomtype, floorNumber, max_capacity, price, F, status)
        return jsonify({"message": result}), 200  # Return success message
        
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {str(e)}"}), 400  # Bad request if parameters are missing

# Route for signing in a new user
# Working
@bp.route('/sign_in', methods=['POST'])
def sign_in():
    try:
        # Extract data from the request
        data = request.json
        user_ID = data.get('user_ID')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        first = data.get('first', 1)  # Default to 1 if not provided

        # Call the sign_in function from models
        result = models.sign_in(user_ID, name, email, password, phone, first)
        return jsonify({"message": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for logging in a user
# Error 500
@bp.route('/log_in', methods=['POST'])
def log_in():
    try:
        data = request.json
        user_ID = data.get('user_ID')
        password = data.get('password')

        result = models.log_in(user_ID, password)
        # shold be return html page for reset password
        if result == "reset":
            return jsonify({"message": "Password reset required."}), 200
        elif result == True:
            return jsonify({"message": "Login successful."}), 200
        elif result == "Invalid password":
            return jsonify({"error": "Invalid password."}), 401
        elif result == "User not found":
            return jsonify({"error": "User not found."}), 404
        else:
            return jsonify({"error": result}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route for editing a user
# Message 200
@bp.route('/edit_user', methods=['PUT'])
def edit_user():
    try:
        # Extract data from the request
        data = request.json
        user_ID = data.get('user_ID')
        name = data.get('name')
        phone = data.get('phone')
        password = data.get('password')
        email = data.get('email')

        # Call the edit_user function from models
        result = models.edit_user(user_ID, name, phone, password, email)
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for inserting a request
# Message 201
@bp.route('/insert_request', methods=['POST'])
def insert_request():
    try:
        # Extract data from the request
        data = request.json
        requests_no = data.get('requests_no')
        request_type = data.get('request_type')
        request_status = data.get('request_status')
        request_details = data.get('request_details')
        room_id = data.get('room_id')
        amount = data.get('amount')

        # Call the insert_request function from models
        result = models.insert_request(requests_no, request_type, request_status, request_details, room_id, amount)
        return jsonify({"message": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for checking out a customer
# Return 200
@bp.route('/check_out', methods=['PUT'])
def check_out():
    try:
        data = request.json
        registration_number = data.get('registration_number')
        result = models.Check_out(registration_number)
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route for show all registration in a customer
# Return 200
@bp.route('/registrationAll', methods=['GET'])
def show_all_registration():
    try:
        all_registration = models.show_all_registration()
        return jsonify([dict(row) for row in all_registration]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Route for sarch a customer by name
# IDK Return 404
@bp.route('/sarch/<int:costomer_name>', methods=['GET'])
def sherch_costomer(costomer_name):
    try:
        all_registration = models.search_customer(costomer_name)
        return jsonify([dict(row) for row in all_registration]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route to search customer by ID
# Return line 237 --> 404
@bp.route('/customer/<int:customer_id>', methods=['GET'])
def search_customer(customer_id):
    try:
        result = models.sherch_coustomer_id(customer_id)
        if isinstance(result, str):  # Handle "Customer not found" or error message
            return jsonify({"message": result}), 404
        return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to search registration by ID
# Return line 249 --> 404
@bp.route('/registration/<int:registration_id>', methods=['GET'])
def search_registration(registration_id):
    try:
        result = models.sherch_registration_id(registration_id)
        if isinstance(result, str):  # Handle "Registration not found" or error message
            return jsonify({"message": result}), 404
        return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to search requests by ID
# Return line 261 --> 404
@bp.route('/request/<int:request_id>', methods=['GET'])
def search_request(request_id):
    try:
        result = models.sherch_requests_by_id(request_id)
        if len(result) == 0:
            return jsonify({"message": "Request not found."}), 404
        return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to update the status of a request
# Return 400 
@bp.route('/request/<int:request_id>/status', methods=['PUT'])
def update_request_status(request_id):
    try:
        result = models.updata_status_requests(request_id)
        if "successfully" in result:
            return jsonify({"message": result}), 200
        return jsonify({"message": result}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
