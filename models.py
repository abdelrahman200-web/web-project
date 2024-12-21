import pyodbc
# connect to database
server = 'localhost\\SQLEXPRESS'  
database = 'softwareDB'
conn_str = 'DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=softwareDB;Trusted_Connection=yes;'
try:
        connection = pyodbc.connect(conn_str)
        pointer=connection.cursor()
        # to show the count id mul data for dashbord
        #route
        def dashbord():
                    Room_count = pointer.execute("SELECT COUNT(*) FROM Room").fetchone()[0]
                    Ready_room = pointer.execute("SELECT COUNT(*) FROM Room WHERE status = 'Ready'").fetchone()[0]
                    registration_number = pointer.execute("SELECT COUNT(*) FROM registration").fetchone()[0]
                    Requests_number = pointer.execute("SELECT COUNT(*) FROM Requests").fetchone()[0]
                    Complaints_number = pointer.execute("SELECT COUNT(*) FROM Complaints").fetchone()[0]
                    return Ready_room , Room_count , registration_number , Requests_number , Complaints_number
        
        # add new registration
        # we shold add the status in request 
        #route
        def add_registration( Id, CheckInDate, CheckOutDate, TotalAmount, PaidAmount, RemainingAmount, StayDuration, 
                             accommodation, note, customer, RoomNo, status):
                try:
                        query = f"""
                         INSERT INTO registration (
                          Id, CheckInDate, CheckOutDate, TotalAmount, PaidAmount, RemainingAmount, 
                         StayDuration, accommodation, note, customer, RoomNo, status
                         )
                         VALUES (
                                   {Id}, '{CheckInDate}', '{CheckOutDate}', {TotalAmount}, {PaidAmount}, {RemainingAmount}, 
                                   '{StayDuration}', '{accommodation}', '{note}', {customer}, {RoomNo}, '{status}'
                          )
                         """
                        pointer.execute(query)
                        return 1
                except Exception as e:
                         print(e),0

        # ================================================================
        # ==========================data access for Room =================
        #route
        def add_Room(Room_number , Roomtype , floorNumber , max , price, F , status):
                try:
                        pointer.execute("""
                        INSERT INTO Room (RoomNo, Roomtype, floorNumber, Max, price, F, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (Room_number, Roomtype, floorNumber, max, price, F, status))
                        return ("New Room added successfully."),201
                except Exception as e:
                         print(e),404 
        # route
        def delate_Room(RoomNo):
            try:
                query = "DELATE * FROM Room where RoomNo = ?"
                pointer.execute(query, (RoomNo,))
                connection.commit()
                return f"Room {RoomNo} deleted successfully."
            except Exception as e:
                return f"Error deleting room: {e}"
            #route
        def update_room_info(Room_number, Roomtype, floorNumber, max_capacity, price, F, status):
            try:
                   query = """UPDATE Room 
                   SET Roomtype = ?, floorNumber = ?, Max = ?, price = ?, F = ?, status = ?
                   WHERE RoomNo = ?"""
                   pointer.execute(query, (Roomtype, floorNumber, max_capacity, price, F, status, Room_number))
                   connection.commit()
                   return f"Room {Room_number} updated successfully."
            except Exception as e:
              return f"Error updating room: {e}"
            # ================================================================`
                # frist = 0 becase the frist registration by maneger
              #route
        def sign_in(user_ID, name, email, password, phone, first):
              try:
                 query = "INSERT INTO user (user_ID, name, email, phone, password, first) VALUES (?, ?, ?, ?, ?, ?)"
                 pointer.execute(query, (user_ID, name, email, phone, password, first))
                 connection.commit()
                 return f"User {name} added successfully."
              except Exception as e:
                 return f"Error signing in: {e}"
        # ================================================================
        # shold be check the frist 0 or 1 if 0 shold be reset the password
         #route
        def log_in(user_ID , password):
             try:
              query = "SELECT user_ID, password, first FROM user WHERE user_ID = ?"
              result = pointer.execute(query, (user_ID,)).fetchone()
              if result:
               db_user_id, db_password, first_login = result
               if db_password == password:
                if first_login == 0:
                    return "reset"
                return True
               else:
                return "Invalid password"
              else:
               return "User not found"
             except Exception as e:
              return f"Error during login: {e}"
        #route
        def edit_user(user_ID, name, phone, password, email):
             try:
                 query = """UPDATE user 
                   SET name = ?, phone = ?, password = ?, email = ?
                   WHERE user_ID = ?"""
                 pointer.execute(query, (name, phone, password, email, user_ID))
                 connection.commit()
                 return f"User {user_ID} updated successfully."
             except Exception as e:
              return f"Error editing user: {e}"

            #   this function is celld if the user login the frist time
        def user_frist (user_ID, new_password):
            try:
             query = "UPDATE user SET password = ?, first = 1 WHERE user_ID = ?"
             pointer.execute(query, (new_password, user_ID))
             connection.commit()
             return f"Password for user {user_ID} reset successfully."
            except Exception as e:
               return f"Error resetting password: {e}"        
        # ================================================================
        # ==========================data access for request =================    
        #                      
        def insert_request(requests_no, request_type, request_status, request_details, room_id, amount):
                 try: 
                         query = '''
                         INSERT INTO Requests (Requests_No, request_type, request_status, request_details, RoomID, amount)
                        VALUES (?, ?, ?, ?, ?, ?)
                        '''
                         pointer.execute(query, (requests_no, request_type, request_status, request_details, room_id, amount))
                         return "Request inserted successfully."

                 except Exception as e:
                  print(e) 
        # ================================================================
        #========data access for check out the coustomer =================    
        #   
        def Check_out(Registration_number):
                 try:
                     query = "UPDATE registration SET status = 'check out' WHERE id = ?"
                     pointer.execute(query, (Registration_number,))
                     connection.commit()
                     return f"Registration {Registration_number} successfully checked out."
                 except Exception as e:
                        print(f"Error during check-out: {e}")
        # ================================================================
        # ===data access for fillter the sherch for all the registration in check in and check out =================    
        #   
        def show_all_registration():
                 try:
                     result = pointer.execute("SELECT * FROM registration").fetchall()
                     return result
                 except Exception as e:
                     print(f"Error fetching all registrations: {e}")
                     return []

# show all the customer in check in mode
        #route
        def show_customer_check_in():
            try:
               result = pointer.execute("SELECT * FROM registration WHERE status = 'check in'").fetchall()
               return result
            except Exception as e:
                   print(f"Error fetching customers with check-in status: {e}")
                   return []
# show all the customer in check out mode
#route
        def show_customer_check_out():
          try:
              result = pointer.execute("SELECT * FROM registration WHERE status = 'check out'").fetchall()
              return result
          except Exception as e:
                print(f"Error fetching customers with check-out status: {e}")
                return []
            # ================================================================
        # ===data access for sherch for coustomer by name =================  
        def search_customer(name):
            try:
               query = "SELECT * FROM customer WHERE name = ?"
               result = pointer.execute(query, (name,)).fetchall()
               if len(result) == 0:
                  return "Customer not found."
               return result
            except Exception as e:
                return str(e)

       #    sherch the coutomer by id
        def sherch_coustomer_id(ID):
           try:
             query = "SELECT * FROM customer WHERE id = ?"
             result = pointer.execute(query, (ID,)).fetchall()
             if len(result) == 0:
                return "Customer not found."
             return result
           except Exception as e:
            return str(e)
        # for sherch the registration by ID
        def sherch_registration_id(ID):
              try:
                  query = "SELECT * FROM registration WHERE Id = ?"
                  result = pointer.execute(query, (ID,)).fetchall()
                  if len(result) == 0:
                    return "Registration not found."
                  return result
              except Exception as e:
                 return str(e)

        # sherch for Requests by id
        def sherch_requests_by_id(ID):
            try:
             query = "SELECT * FROM Requests WHERE [Requests-No] = ?"
             result = pointer.execute(query, (ID,)).fetchall()
             return result
            except Exception as e:
                return str(e)

        # updata the status for requests
        def updata_status_requests(ID)  :
           try:
            query = "UPDATE Requests SET [request-status] = 'completed' WHERE Id = ?"
            pointer.execute(query, (ID,))
            connection.commit()
            return "Request status updated successfully."
           except Exception as e:
             return str(e)

                
except Exception as e:
    print(e)  
