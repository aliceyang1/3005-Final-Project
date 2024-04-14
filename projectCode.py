import psycopg2
from getpass import getpass
from psycopg2 import sql
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def connect_db():
    try:
        return psycopg2.connect(
            host="localhost",
            database="fitness_management_system_db",
            user="postgres",
            password="5772570."
        )
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def register_member(connection):
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    email = input("Enter email: ")
    full_name = input("Enter full name: ")
    address = input("Enter address: ")
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Members (Username, Password, Email, FullName, Address, DateOfBirth)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, password, email, full_name, address, date_of_birth))
            connection.commit()
            print("Member registered successfully.")
    except psycopg2.Error as e:
        print(f"Failed to register member: {e}")

def update_member_profile(connection):
    member_id = input("Enter your member ID: ")
    print("\nWhat would you like to update?")
    print("1. Personal Information")
    print("2. Fitness Goals")
    print("3. Health Metrics")
    option = input("Choose an option (1-3): ")

    try:
        if option == "1":
            update_personal_info(connection, member_id)
        elif option == "2":
            update_fitness_goals(connection, member_id)
        elif option == "3":
            update_health_metrics(connection, member_id)
        else:
            print("Invalid option selected.")
    except psycopg2.Error as e:
        print(f"Error updating profile: {e}")

def update_personal_info(connection, member_id):
    email = input("Enter new email: ")
    full_name = input("Enter new full name: ")
    address = input("Enter new address: ")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE Members
            SET Email = %s, FullName = %s, Address = %s
            WHERE Member_ID = %s
        """, (email, full_name, address, member_id))
        connection.commit()
        print("Personal information updated successfully.")

def update_fitness_goals(connection, member_id):
    print("\nFitness Goals Management:")
    print("1. Add a new goal")
    print("2. Delete a goal")
    print("3. Update a goal's status")
    choice = input("Choose an option (1-3): ")

    if choice == "1":
        add_fitness_goal(connection, member_id)
    elif choice == "2":
        delete_fitness_goal(connection, member_id)
    elif choice == "3":
        update_goal_status(connection, member_id)
    else:
        print("Invalid option selected.")

def add_fitness_goal(connection, member_id):
    description = input("Enter goal description: ")
    status = input("Enter initial goal status (e.g., Active, Pending): ")
    deadline = input("Enter goal deadline (YYYY-MM-DD): ")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Goals (Member_ID, Description, Status, Deadline)
            VALUES (%s, %s, %s, %s)
        """, (member_id, description, status, deadline))
        connection.commit()
        print("New fitness goal added successfully.")

def delete_fitness_goal(connection, member_id):
    goal_id = input("Enter the ID of the goal to delete: ")
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM Goals
            WHERE Goal_ID = %s AND Member_ID = %s
        """, (goal_id, member_id))
        connection.commit()
        print("Fitness goal deleted successfully.")

def update_goal_status(connection, member_id):
    goal_id = input("Enter the ID of the goal to update: ")
    new_status = input("Enter the new status of the goal (e.g., Completed, Active): ")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE Goals
            SET Status = %s
            WHERE Goal_ID = %s AND Member_ID = %s
        """, (new_status, goal_id, member_id))
        connection.commit()
        print("Fitness goal status updated successfully.")

def update_health_metrics(connection, member_id):
    print("\nManage Health Metrics:")
    print("1. Add new metric")
    print("2. Update existing metric")
    choice = input("Choose an option (1-2): ")

    if choice == "1":
        add_health_metric(connection, member_id)
    elif choice == "2":
        update_existing_metric(connection, member_id)
    else:
        print("Invalid option selected.")

def add_health_metric(connection, member_id):
    metric_type = input("Enter new metric type (e.g., Weight, Blood Pressure): ")
    value = input("Enter metric value: ")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO HealthMetrics (Member_ID, MetricType, Value)
            VALUES (%s, %s, %s)
        """, (member_id, metric_type, value))
        connection.commit()
        print("New health metric added successfully.")

def update_existing_metric(connection, member_id):
    print("Fetching available metrics...")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Metric_ID, MetricType, Value FROM HealthMetrics
            WHERE Member_ID = %s
        """, (member_id,))
        metrics = cursor.fetchall()

        if not metrics:
            print("No metrics found to update.")
            return

        for metric in metrics:
            print(f"ID: {metric[0]}, Type: {metric[1]}, Current Value: {metric[2]}")

        metric_id = input("Enter the ID of the metric to update: ")
        new_value = input("Enter the new value: ")

        cursor.execute("""
            UPDATE HealthMetrics
            SET Value = %s
            WHERE Metric_ID = %s AND Member_ID = %s
        """, (new_value, metric_id, member_id))
        connection.commit()
        print("Health metric updated successfully.")


def display_member_dashboard(connection, member_id):
    try:
        with connection.cursor() as cursor:
            # Fetch basic member info
            cursor.execute("""
                SELECT Username, FullName, Email FROM Members
                WHERE Member_ID = %s
            """, (member_id,))
            member_info = cursor.fetchone()
            if member_info is None:
                print("No member found with the provided ID.")
                return
            
            print("\nMember Dashboard:")
            print(f"Username: {member_info[0]}, Full Name: {member_info[1]}, Email: {member_info[2]}")

            # Fetch exercise routines using a JOIN operation if a join table exists
            cursor.execute("""
                SELECT RoutineName, Description, DifficultyLevel FROM ExerciseRoutines
                JOIN Members_Routines ON ExerciseRoutines.Routine_ID = Members_Routines.Routine_ID
                WHERE Member_ID = %s
            """, (member_id,))
            routines = cursor.fetchall()
            print("\nExercise Routines:")
            if routines:
                for routine in routines:
                    print(f"Routine Name: {routine[0]}, Description: {routine[1]}, Difficulty: {routine[2]}")
            else:
                print("No exercise routines found.")

            # Fetch fitness goals
            cursor.execute("""
                SELECT Description, Status, Deadline FROM Goals
                WHERE Member_ID = %s
            """, (member_id,))
            goals = cursor.fetchall()
            print("\nFitness Goals:")
            if goals:
                for goal in goals:
                    print(f"Goal: {goal[0]}, Status: {goal[1]}, Deadline: {goal[2]}")
            else:
                print("No fitness goals found.")

            # Fetch health metrics
            cursor.execute("""
                SELECT MetricType, Value FROM HealthMetrics
                WHERE Member_ID = %s
            """, (member_id,))
            metrics = cursor.fetchall()
            print("\nHealth Metrics:")
            if metrics:
                for metric in metrics:
                    print(f"Metric: {metric[0]}, Value: {metric[1]}")
            else:
                print("No health metrics found.")

    except psycopg2.Error as e:
        print(f"Failed to retrieve member data: {e}")



def schedule_management(connection):
    member_id = input("Enter member ID: ")
    datetime_str = input("Enter session date and time (YYYY-MM-DD HH:MM): ")
    session_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    trainer_id = input("Enter trainer ID: ")

    try:
        with connection.cursor() as cursor:
            # Check trainer availability first
            cursor.execute("""
                SELECT * FROM Sessions WHERE Trainer_ID = %s AND DateTime = %s
            """, (trainer_id, session_datetime))
            if cursor.fetchone():
                print("This trainer is not available at the specified time.")
                return
            # Schedule session
            cursor.execute("""
                INSERT INTO Sessions (DateTime, Status, Member_ID, Trainer_ID)
                VALUES (%s, 'Scheduled', %s, %s)
            """, (session_datetime, member_id, trainer_id))
            connection.commit()
            print("Session scheduled successfully.")
    except psycopg2.Error as e:
        print(f"Failed to schedule session: {e}")

def set_trainer_availability(connection, trainer_id):
    print("Setting Trainer Availability:")
    date = input("Enter date for availability (YYYY-MM-DD): ")
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")

    try:
        with connection.cursor() as cursor:
            # Insert into Availabilities
            cursor.execute("""
                INSERT INTO Availabilities (DateTime)
                VALUES (TO_TIMESTAMP(%s || ' ' || %s, 'YYYY-MM-DD HH24:MI'))
                RETURNING Availability_ID
            """, (date, start_time))
            availability_id = cursor.fetchone()[0]

            # Link the availability to the trainer
            cursor.execute("""
                INSERT INTO Trainers_Availabilities (Trainer_ID, Availability_ID)
                VALUES (%s, %s)
            """, (trainer_id, availability_id))
            connection.commit()
            print("Availability set successfully for %s to %s on %s." % (start_time, end_time, date))
    except psycopg2.Error as e:
        print(f"Error setting availability: {e}")


def view_member_profile(connection):
    member_name = input("Enter member's name to search: ")

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Member_ID, FullName, Email FROM Members
                WHERE FullName ILIKE %s
            """, ('%' + member_name + '%',))
            members = cursor.fetchall()
            if members:
                print("\nMember Profiles Found:")
                for member in members:
                    print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}")
            else:
                print("No members found with that name.")
    except psycopg2.Error as e:
        print(f"Error retrieving member profiles: {e}")

def main():
    connection = connect_db()
    if connection is None:
        return
    
    print("Welcome to the Health and Fitness Club Management System")
    while True:
        print("\nIdentify your role:")
        print("1. Member")
        print("2. Trainer")
        print("3. Administrative Staff")
        print("4. Exit")
        role_choice = input("Enter your role (1-3) or exit (4): ")

        if role_choice == "1":
            member_id = input("Enter your member ID: ")
            member_menu(connection, member_id)
        elif role_choice == "2":
            trainer_id = input("Enter your trainer ID: ")
            trainer_menu(connection, trainer_id)
        elif role_choice == "3":
            admin_id = input("Enter your admin ID: ")
            admin_menu(connection, admin_id)
        elif role_choice == "4":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
    connection.close()

def member_menu(connection, member_id):
    while True:
        print("\nMember Dashboard")
        print("1. Register")
        print("2. Update Profile")
        print("3. View Dashboard")
        print("4. Schedule a Session")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            register_member(connection)
        elif choice == "2":
            update_member_profile(connection, member_id)
        elif choice == "3":
            display_member_dashboard(connection, member_id)
        elif choice == "4":
            schedule_management(connection)
        elif choice == "5":
            print("Returning to main menu.")
            break
        else:
            print("Invalid option. Please try again.")

def trainer_menu(connection, trainer_id):
    while True:
        print("\nTrainer Dashboard")
        print("1. Set Availability")
        print("2. View Member Profile")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            set_trainer_availability(connection, trainer_id)
        elif choice == "2":
            view_member_profile(connection)
        elif choice == "3":
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice, please try again.")

def view_bookings(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Session_ID, DateTime, Room_ID, Member_ID, Trainer_ID
            FROM Sessions
            WHERE Room_ID IS NOT NULL
            ORDER BY DateTime
        """)
        bookings = cursor.fetchall()
        if bookings:
            print("Current Bookings:")
            for booking in bookings:
                print(f"Session ID: {booking[0]}, Date/Time: {booking[1]}, Room ID: {booking[2]}, Member ID: {booking[3]}, Trainer ID: {booking[4]}")
        else:
            print("No bookings found.")


def add_booking(connection):
    room_id = input("Enter room ID: ")
    member_id = input("Enter member ID: ")
    trainer_id = input("Enter trainer ID: ")
    datetime_str = input("Enter date and time for the booking (YYYY-MM-DD HH:MM): ")

    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                INSERT INTO Sessions (DateTime, Room_ID, Member_ID, Trainer_ID, Status)
                VALUES (TO_TIMESTAMP(%s, 'YYYY-MM-DD HH24:MI'), %s, %s, %s, 'Scheduled')
            """, (datetime_str, room_id, member_id, trainer_id))
            connection.commit()
            print("Booking added successfully.")
        except psycopg2.Error as e:
            print(f"Failed to add booking: {e}")
            connection.rollback()

def cancel_booking(connection):
    session_id = input("Enter the session ID to cancel: ")

    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                DELETE FROM Sessions
                WHERE Session_ID = %s
            """, (session_id,))
            if cursor.rowcount:
                connection.commit()
                print("Booking cancelled successfully.")
            else:
                print("No booking found with that session ID.")
        except psycopg2.Error as e:
            print(f"Failed to cancel booking: {e}")
            connection.rollback()

def view_equipment_status(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Equipment_ID, EquipmentName, Status, LastMaintenanceDate
            FROM Equipment
            ORDER BY Equipment_ID
        """)
        equipments = cursor.fetchall()
        if equipments:
            print("Equipment Status Overview:")
            for equipment in equipments:
                print(f"Equipment ID: {equipment[0]}, Name: {equipment[1]}, Status: {equipment[2]}, Last Maintenance: {equipment[3]}")
        else:
            print("No equipment found.")

def record_payment(connection):
    member_id = input("Enter the member ID who is making the payment: ")
    amount = input("Enter the amount: ")
    payment_method = input("Enter the payment method (e.g., Credit Card, PayPal): ")
    description = input("Enter the payment description: ")
    payment_date = input("Enter the payment date (YYYY-MM-DD): ")

    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                INSERT INTO Payments (Member_ID, Amount, PaymentMethod, Description, PaymentDate)
                VALUES (%s, %s, %s, %s, %s)
            """, (member_id, amount, payment_method, description, payment_date))
            connection.commit()
            print("Payment recorded successfully.")
        except psycopg2.Error as e:
            print(f"Failed to record payment: {e}")
            connection.rollback()

def view_outstanding_payments(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Payment_ID, Member_ID, Amount, PaymentDate, Description
            FROM Payments
            WHERE Status = 'Outstanding'
            ORDER BY PaymentDate
        """)
        payments = cursor.fetchall()
        if payments:
            print("\nOutstanding Payments:")
            for payment in payments:
                print(f"Payment ID: {payment[0]}, Member ID: {payment[1]}, Amount: {payment[2]}, Date: {payment[3]}, Description: {payment[4]}")
        else:
            print("No outstanding payments found.")

def update_equipment_status(connection):
    equipment_id = input("Enter the equipment ID to update: ")
    
    with connection.cursor() as cursor:
        # Fetch current equipment details to show to the user before they make an update.
        cursor.execute("""
            SELECT Equipment_ID, EquipmentName, Status, LastMaintenanceDate
            FROM Equipment
            WHERE Equipment_ID = %s
        """, (equipment_id,))
        equipment = cursor.fetchone()

        if equipment:
            print(f"Current Equipment Details — ID: {equipment[0]}, Name: {equipment[1]}, Status: {equipment[2]}, Last Maintenance: {equipment[3]}")
        else:
            print("Equipment not found.")
            return

        new_status = input("Enter new status (Available, Maintenance, Out of Service, etc.): ")
        new_maintenance_date = input("Enter the new maintenance date (YYYY-MM-DD), if applicable: ")

        try:
            if new_maintenance_date:
                cursor.execute("""
                    UPDATE Equipment
                    SET Status = %s, LastMaintenanceDate = TO_DATE(%s, 'YYYY-MM-DD')
                    WHERE Equipment_ID = %s
                """, (new_status, new_maintenance_date, equipment_id))
            else:
                cursor.execute("""
                    UPDATE Equipment
                    SET Status = %s
                    WHERE Equipment_ID = %s
                """, (new_status, equipment_id))
            connection.commit()
            print("Equipment status updated successfully.")
        except psycopg2.Error as e:
            print(f"Failed to update equipment status: {e}")
            connection.rollback()

def monitor_equipment_maintenance(connection):
    print("Equipment Maintenance Monitoring:")
    print("1. View Equipment Status")
    print("2. Update Equipment Status")
    choice = input("Choose an action: ")
    if choice == "1":
        view_equipment_status(connection)
    elif choice == "2":
        update_equipment_status(connection)
    else:
        print("Invalid option selected.")

def process_payments(connection):
    print("Processing Payments:")
    print("1. View Outstanding Payments")
    print("2. Record Payment")
    choice = input("Choose an action: ")
    if choice == "1":
        view_outstanding_payments(connection)
    elif choice == "2":
        record_payment(connection)
    else:
        print("Invalid option selected.")

def view_class_schedule(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Classes.Class_ID, Classes.ClassName, Classes.DateTime, Rooms.RoomName, Trainers.FullName
            FROM Classes
            JOIN Rooms ON Classes.Room_ID = Rooms.Room_ID
            JOIN Trainers ON Classes.Trainer_ID = Trainers.Trainer_ID
            ORDER BY Classes.DateTime
        """)
        classes = cursor.fetchall()
        if classes:
            print("\nCurrent Class Schedule:")
            for cls in classes:
                print(f"Class ID: {cls[0]}, Name: {cls[1]}, Date/Time: {cls[2]}, Room: {cls[3]}, Trainer: {cls[4]}")
        else:
            print("No classes found.")

def modify_class_schedule(connection):
    class_id = input("Enter the class ID to modify: ")

    with connection.cursor() as cursor:
        # Display current class details
        cursor.execute("""
            SELECT Class_ID, ClassName, DateTime, Room_ID, Trainer_ID
            FROM Classes
            WHERE Class_ID = %s
        """, (class_id,))
        class_info = cursor.fetchone()

        if class_info:
            print(f"Current Details — ID: {class_info[0]}, Name: {class_info[1]}, DateTime: {class_info[2]}, Room ID: {class_info[3]}, Trainer ID: {class_info[4]}")
        else:
            print("Class not found.")
            return
        
        print("Options to modify the class:")
        print("1. Change Date/Time")
        print("2. Change Room")
        print("3. Change Trainer")
        print("4. Cancel Class")
        option = input("Select an action: ")

        try:
            if option == "1":
                new_datetime = input("Enter new date and time (YYYY-MM-DD HH:MM): ")
                cursor.execute("""
                    UPDATE Classes
                    SET DateTime = TO_TIMESTAMP(%s, 'YYYY-MM-DD HH24:MI')
                    WHERE Class_ID = %s
                """, (new_datetime, class_id))
                print("Class schedule updated successfully.")
            elif option == "2":
                new_room_id = input("Enter new room ID: ")
                cursor.execute("""
                    UPDATE Classes
                    SET Room_ID = %s
                    WHERE Class_ID = %s
                """, (new_room_id, class_id))
                print("Room updated successfully.")
            elif option == "3":
                new_trainer_id = input("Enter new trainer ID: ")
                cursor.execute("""
                    UPDATE Classes
                    SET Trainer_ID = %s
                    WHERE Class_ID = %s
                """, (new_trainer_id, class_id))
                print("Trainer updated successfully.")
            elif option == "4":
                cursor.execute("""
                    DELETE FROM Classes
                    WHERE Class_ID = %s
                """, (class_id,))
                print("Class cancelled successfully.")
            connection.commit()
        except psycopg2.Error as e:
            print(f"Failed to modify class schedule: {e}")
            connection.rollback()

def update_class_schedules(connection):
    print("Updating Class Schedules:")
    print("1. View Current Schedule")
    print("2. Modify Schedule")
    choice = input("Choose an action: ")
    if choice == "1":
        view_class_schedule(connection)
    elif choice == "2":
        modify_class_schedule(connection)
    else:
        print("Invalid option selected.")

def manage_room_bookings(connection):
    print("Room Booking Management:")
    print("1. View Bookings")
    print("2. Add Booking")
    print("3. Cancel Booking")
    choice = input("Choose an action: ")
    if choice == "1":
        view_bookings(connection)
    elif choice == "2":
        add_booking(connection)
    elif choice == "3":
        cancel_booking(connection)
    else:
        print("Invalid option selected.")


def admin_menu(connection, admin_id):
    while True:
        print("\nAdmin Dashboard")
        print("1. Manage Room Bookings")
        print("2. Monitor Equipment Maintenance")
        print("3. Update Class Schedules")
        print("4. Process Payments")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            manage_room_bookings(connection)
        elif choice == "2":
            monitor_equipment_maintenance(connection)
        elif choice == "3":
            update_class_schedules(connection)
        elif choice == "4":
            process_payments(connection)
        elif choice == "5":
            print("Returning to main menu.")
            break
        else:
            print("Invalid option. Please try again.")



if __name__ == "__main__":
    main()