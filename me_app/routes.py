from flask import Blueprint, request, jsonify, render_template, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import models as models
bp=Blueprint("route",__name__)

# ===========================================================================
# route for pages template
# ===========================================================================
# Route for show all elelmnt for dashboard regsitration
@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@bp.route('/dashboard/registration', methods=['GET'])
def get_dashboard_registration():
    try:
        total_hotel_register, Order, Issues, Order_completed, Complaints_number,Check_out = models.dashbord_for_registration()
        registration,s = models.show_all_registration()
        return render_template('pages/show-registration.html',total_hotel_register=total_hotel_register , order_count = Order , Issues_count =  Issues ,
                                total_oredr_completed = Order_completed  , Requests = Complaints_number , complaints_num = Check_out , registration=registration) , 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@bp.route('/home', methods=['GET'])
def home():
    Ready_room, Room_count, registration_number, Requests_number, Complaints_number,check_out = models.dashbord()
    return render_template('pages/home.html',total_hotel_rooms =Room_count , Ready_room = Ready_room , 
                           check_in_no = registration_number,check_out_no = check_out, complaints_num = Complaints_number ,
                           Requests = Requests_number)

@bp.route('/login', methods=['GET'])
def login():
    return render_template('pages/login.html')

@bp.route('/register-customer', methods=['GET'])
def page_register_customer():
    return render_template('pages/Registration-costomer.html')

@bp.route('/rooms', methods=['GET'])
def page_rooms():
    return render_template('pages/Rooms.html')

@bp.route('/show-customer', methods=['GET'])
def page_show_customer():
    return render_template('pages/show-insert-customer.html')

@bp.route('/signin', methods=['GET'])
def page_signin():
    return render_template('pages/singin.html')


# ===========================================================================
# ===========================================================================

# Route to add a new registration
# Returns Else statement response
@bp.route('/register', methods=['POST'])
def register_customer():
    
    try:
        data = request.json
        result = models.add_registration(
            Id=data['Id'], #interger
            CheckInDate=data['CheckInDate'], #date
            CheckOutDate=data['CheckOutDate'], #date
            TotalAmount=data['TotalAmount'], #interger
            PaidAmount=data['PaidAmount'], #interger
            RemainingAmount=data['RemainingAmount'], #interger
            StayDuration=data['StayDuration'], #text
            accommodation=data['accommodation'], # text
            note=data['note'], #text 
            customer_ID = data['customer_ID'], #interger # make shure the ID for customer is placed in database for customer
            RoomNo=data['RoomNo'], #interger # make shure the ID for RoomNo is placed in database for RoomNo
            status='check in' #text
        )
        if result==1:
            return jsonify({"Registration added successfully."}), 201
        else:
            return jsonify({"error": "An error occurred while processing the request."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Route to delete a room by RoomNo
@bp.route('/room/delate/<Room_number>', methods=['DELETE'])
def delete_room(Room_number):
    try:
        m , S=models.delate_Room(Room_number) 
        if m:
            return jsonify({"message": "Room deleted successfully."}), S
        else:
            return jsonify({"error": "An error occurred while processing the request."}), S
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# route to return the data for dashboard
#No Problem
@bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    try:
        Ready_room, Room_count, registration_number, Requests_number, Complaints_number,check_out = models.dashbord()
        response = {
            "Ready_room": Ready_room,
            "Room_count": Room_count,
            "registration_number": registration_number,
            "Requests_number": Requests_number,
            "Complaints_number": Complaints_number,
            "check_out": check_out
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get customers who are checked in
# Returns [] empty 
@bp.route('/customers/checkin', methods=['GET'])
def get_customers_check_in():
    try:
        # Call show_customer_check_in from models to get the registration data
        customers_check_in = models.show_customer_check_in()
        # If the result is an error message, return it as an error response
        if isinstance(customers_check_in, str):
            return jsonify({"error": customers_check_in}), 500
        # Manually map rows to a dictionary with customer and registration details
        customers = []
        for row in customers_check_in:
            customer_dict = {
                "registration_id": row[0],          # registration Id
                "check_in_date": row[1],             # Check-in Date
                "check_out_date": row[2],            # Check-out Date
                "total_amount": row[3],              # Total Amount
                "paid_amount": row[4],               # Paid Amount
                "remaining_amount": row[5],          # Remaining Amount
                "stay_duration": row[6],             # Stay Duration
                "accommodation": row[7],             # Accommodation
                "note": row[8],                     # Note
                "customer_name": row[9],            # Customer's name
                "customer_phone": row[10],          # Customer's phone
            }
            customers.append(customer_dict)
        
        return jsonify(customers), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get customers who have checked out
@bp.route('/customers/checkout', methods=['GET'])
def get_customers_check_out():
    try:
        customers_check_out = models.show_customer_check_out()
        if isinstance(customers_check_out, str):
            return jsonify({"error": customers_check_out}), 500
        customers = []
        for row in customers_check_out:
            customer_dict = {
                "registration_id": row[0],          # registration Id
                "check_in_date": row[1],             # Check-in Date
                "check_out_date": row[2],            # Check-out Date
                "total_amount": row[3],              # Total Amount
                "paid_amount": row[4],               # Paid Amount
                "remaining_amount": row[5],          # Remaining Amount
                "stay_duration": row[6],             # Stay Duration
                "accommodation": row[7],             # Accommodation
                "note": row[8],                     # Note
                "customer_name": row[9],            # Customer's name
                "customer_phone": row[10],          # Customer's phone
            }
            customers.append(customer_dict)

        # Return the data as a JSON response
        return jsonify(customers), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Route to handle room addition
@bp.route('/addroom', methods=['POST'])
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
        max_capacity = data['max']
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
def show_all_registration_route():
    try:
        # Fetch the result and status code from the model function
        result, status_code = models.show_all_registration()  
        if status_code != 200:
            return jsonify({"message": "No registrations found."}), status_code         
        # Map the database rows to dictionaries with relevant fields
        registrations = [
            {
                "id": row[0], 
                "check_in_date": row[1], 
                "check_out_date": row[2], 
                "total_amount": row[3], 
                "paid_amount": row[4], 
                "remaining_amount": row[5],
                "stay_duration": row[6],
                "accommodation": row[7],
                "note": row[8],
                "customer_id": row[9],
                "room_no": row[10],
                "status": row[11]
            }
            for row in result
        ]        
        return jsonify(registrations), status_code  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Route for sarch a customer by name
# IDK Return 404
@bp.route('/sarch/<costomer_name>', methods=['GET'])
def sherch_costomer(costomer_name):
    try:
        all_registration, status_code = models.search_customer(costomer_name)
        if status_code != 200:
            return jsonify({"message": "No customers found."}), status_code
        customers = [
            {
                "identity": row[0], 
                "name": row[1], 
                "phone": row[2], 
                "another_phone": row[3],
                "age": row[4], 
                "email": row[5], 
                "nationality": row[6], 
                "type_of_proof_of": row[7]
            }
            for row in all_registration
        ]        
        # Return the result as a JSON response
        return jsonify(customers), status_code  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
# Route to search customer by ID
@bp.route('/customer/<int:customer_id>', methods=['GET'])
def search_customer(customer_id):
    try:
        data, status_code = models.sherch_coustomer_id(customer_id)
        if status_code == 404:
            return jsonify({"error": data}), 404        
        return jsonify(data), status_code 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to search registration by ID
@bp.route('/registration/<int:registration_id>', methods=['GET'])
def search_registration(registration_id):
    try:
        result = models.sherch_registration_id(registration_id)
        
        if isinstance(result, str):  # Handle "Registration not found" or error message
            return jsonify({"message": result}), 404
        
        # Convert the result to a dictionary if it's a tuple
        columns = ["Id", "CheckInDate", "CheckOutDate", "TotalAmount", "PaidAmount", 
                   "RemainingAmount", "StayDuration", "accommodation", "note", 
                   "customer", "RoomNo", "status"]
        
        registration_data = [
            dict(zip(columns, row)) for row in result
        ]
        
        return jsonify(registration_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to search requests by ID
# Return line 261 --> 404
@bp.route('/request/<int:request_id>', methods=['GET'])
def search_request(request_id):
    try:
        result = models.sherch_requests_by_id(request_id)
        if not result:
            return jsonify({"message": "Request not found."}), 404
        columns = ["Requests-No", "request-type", "request-status", "request-details", "RoomID", "amount"]
        requests_data = [dict(zip(columns, row)) for row in result]
        return jsonify(requests_data), 200  # Return the result as a JSON response
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
    
# Route to show all rooms
@bp.route('/show_rooms', methods=['GET'])
def show_all_rooms_route():
    try:
        result, status_code = models.show_all_room() 
        if not result:
            return jsonify({"message": "No rooms found."}), 404 
        rooms = [
            {key: value for key, value in zip(["RoomNo", "Roomtype", "floorNumber", "Max", "price", "F", "status"], row)}
            for row in result
        ]
        return jsonify(rooms), status_code  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route to add new customer
@bp.route('/add_customer', methods=['POST', 'GET'])
def add_customer_route():
    print(request.method)  # Check what method is being received
    data = request.get_json()
    try:
        identity = data['identity']
        name = data['name']
        phone = data['phone']
        another_phone = data.get('another-phone', None)
        age = data['age']
        email = data.get('email', None)
        nationality = data['nationality']
        type_of_proof_of = data['type_of_proof_of']
        success = models.add_customer(identity, name, phone, another_phone, age, email, nationality, type_of_proof_of)
        if success:
            return jsonify({"message": "Customer added successfully!"}), 201
        else:
            return jsonify({"message": "Error adding customer."}), 500

    except KeyError as e:
        return jsonify({"message": f"Missing required field: {str(e)}"}), 400
# Route to show all customers
@bp.route('/customers', methods=['GET'])
def show_all_customers_route():
    try:
        result, status_code = models.get_customers()  
        if status_code != 200:
            return jsonify({"message": "No customers found."}), status_code 
        customers = [
            {"identity": row[0], "name": row[1], "phone": row[2], "another_phone": row[3],
             "age": row[4], "email": row[5], "nationality": row[6], "type_of_proof_of": row[7]}
            for row in result
        ]
        return jsonify(customers), status_code  

    except Exception as e:
        return jsonify({"error": str(e)}), status_code
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/set_cookie', methods=['GET'])
def set_cookie():
    try:
        # Create a response object
        response = make_response(jsonify({"message": "Cookie has been set!"}))
        
        # Set the cookie (key, value)
        response.set_cookie('user_id', '12345', max_age=60*60*24, httponly=True)  # Cookie lasts 1 day
        
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ===========================================================================
# ===========================================================================


# s = URLSafeTimedSerializer(bp.secret_key)



# @bp.route('/send-reset-link', methods=['POST'])
# def send_reset_link():
#     data = request.json
#     email = data.get('email')
#     # Generate a secure token
#     token = s.dumps(email, salt='password-reset-salt')

#     # Create the reset link
#     reset_link = url_for('reset_password', token=token, _external=True)

#     # Send the email
#     msg = Message('Password Reset Request', sender='bsyd654@gmail.com', recipients=[email])
#     msg.body = f"Click the link to reset your password: {reset_link}"
#     mail.send(msg)

#     return jsonify({"message": "Reset link sent to your email."}), 200

# @bp.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password_route(token):
#     try:
#         email = s.loads(token, salt='password-reset-salt', max_age=3600)  # 1-hour token expiry
#     except SignatureExpired:
#         return "The reset link has expired!", 400
#     except Exception as e:
#         return f"An error occurred: {e}", 400

#     if request.method == 'POST':
#         new_password = request.form.get('password')
#         if not new_password:
#             return "Password is required.", 400
        
#         # Call the reset password function to update the database
#         result = models.reset_password(email, new_password)
#         if result == 1:  # Successful password reset
#             return "Password updated successfully!", 200
#         else:
#             return f"Error updating password: {result}", 500

#     # Render password reset form
#     return render_template('new_password.html', email=email)