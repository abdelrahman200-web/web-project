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
                    Check_out = pointer.execute("SELECT COUNT(*) FROM registration WHERE status = 'check out'").fetchone()[0]
                    return Ready_room , Room_count , registration_number , Requests_number , Complaints_number , Check_out
        
        def dashbord_for_registration():
                    total_hotel_register = pointer.execute("SELECT COUNT(*) FROM registration").fetchone()[0]
                    Order = pointer.execute("SELECT COUNT(*) FROM Requests").fetchone()[0]
                    Issues = pointer.execute("SELECT COUNT(*) FROM Complaints").fetchone()[0]
                    Order_completed = pointer.execute("SELECT COUNT(*) FROM Requests WHERE [request-status] ='completed'").fetchone()[0]
                    Complaints_number = pointer.execute("SELECT COUNT(*) FROM Complaints").fetchone()[0]
                    Check_out = pointer.execute("SELECT COUNT(*) FROM registration WHERE status = 'check out'").fetchone()[0]
                    return total_hotel_register , Order , Issues , Order_completed , Complaints_number , Check_out
        
        # add new registration
        # we shold add the status in request 
        #route
        def add_registration(Id, CheckInDate, CheckOutDate, TotalAmount, PaidAmount, RemainingAmount, StayDuration, accommodation, note, customer_ID, RoomNo, status):
            try:
                 query = '''
            INSERT INTO registration (
                Id, CheckInDate, CheckOutDate, TotalAmount, PaidAmount,
                RemainingAmount, StayDuration, accommodation, note,
                customer, RoomNo, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
                 pointer.execute(query, (Id, CheckInDate, CheckOutDate, TotalAmount, PaidAmount,
                                RemainingAmount, StayDuration, accommodation, note,
                                customer_ID, RoomNo, status))
                 connection.commit()
                 return True
            except Exception as e:
              print(f"Error in add_registration: {e}")
              return False
        
        # ================================================================
        # ==========================data access for Room =================
        #route
        def add_Room(Room_number , Roomtype , floorNumber , max , price, F , status):
                try:
                        pointer.execute("""
                        INSERT INTO Room (RoomNo, Roomtype, floorNumber, Max, price, F, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (Room_number, Roomtype, floorNumber, max, price, F, status))
                        connection.commit()                        
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
        def reset_password (user_ID, new_password):
            try:
             query = "UPDATE user SET password = ?, first = 1 WHERE user_ID = ?"
             pointer.execute(query, (new_password, user_ID))
             connection.commit()
             return 1
            except Exception as e:
               return f"Error resetting password: {e}"        
        # ================================================================
        # ==========================data access for request =================    
        #          
        # route            
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
        #route
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
        #route
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
        # route
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
        #route
        def sherch_coustomer_id(ID):
          try:
              query = "SELECT * FROM customer WHERE [identity] = ?"
              result = pointer.execute(query, (ID,)).fetchall()
              if len(result) == 0:
                 return "Customer not found.", 404
              columns = [desc[0] for desc in pointer.description]  
              result_dict = [dict(zip(columns, row)) for row in result]        
              return result_dict, 200
          except Exception as e:
              return str(e), 404
        # for sherch the registration by ID
        #route
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
        #route
        def sherch_requests_by_id(ID):
            try:
             query = "SELECT * FROM Requests WHERE [Requests-No] = ?"
             result = pointer.execute(query, (ID,)).fetchall()
             return result
            except Exception as e:
                return str(e)

        # updata the status for requests
        #route
        def updata_status_requests(ID)  :
           try:
            query = "UPDATE Requests SET [request-status] = 'completed' WHERE Id = ?"
            pointer.execute(query, (ID,))
            connection.commit()
            return "Request status updated successfully."
           except Exception as e:
             return str(e)
        #route
        
        def show_all_room():
            try:
                result = pointer.execute("SELECT * FROM Room").fetchall()
                return result,200
            except Exception as e:
                return str(e),404

        #route
        def add_customer(identity, name, phone, another_phone, age, email, nationality, type_of_proof_of):
               try:
                   insert_sql = """
                INSERT INTO dbo.customer 
                ([identity], [name], [phone], [another-phone], [age], [email], [nationality], [type-of-proof-of]) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                  """
                   pointer.execute(insert_sql, (identity, name, phone, another_phone, age, email, nationality, type_of_proof_of))
                   connection.commit()
                   return "Customer added successfully."
               except Exception as e:
                 print(f"Error: {e}")
         #route     
         # show all the customer   
        def get_customers():
          try:
              pointer.execute("SELECT * FROM customer")
              customers = pointer.fetchall()
              return customers,200
          except Exception as e:
                return str(e),404

except Exception as e:
    print(e)  
