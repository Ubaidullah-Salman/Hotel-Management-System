import json
import os
from datetime import datetime

def display_title():
    print("\n" * 2)
    print("=" * 40)
    print("""
          HOTEL MANAGEMENT SYSTEM
    """)
    print("=" * 40)
    print("\n" * 2)

data_file = 'hotel_data.json'

def save_data(rooms, bookings):
    with open(data_file, 'w') as file:
        json.dump({"rooms": rooms, "bookings": bookings}, file, indent=4)
    print("Data saved successfully")

def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            data = json.load(file)
            return data.get("rooms", []), data.get("bookings", [])
    return [], []

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

rooms = []
bookings = []
def add_room(rooms):
    try:
        room_no = int(input("Enter the room number: "))
        room_type = input("Enter the type of room: ")
        price = int(input("Enter the price of room: "))

        room_details = {"room_number": room_no, 'Type': room_type, 'price': price, 'availability': True}

        if any(r['room_number'] == room_no for r in rooms):
            print("Room Number already registered, Please try again")

        else:
            rooms.append(room_details)
            print("Room added successfully!")
            save_data(rooms, bookings)
    except ValueError:
        print("Invalid Input, Please enter Integer value")

def view_rooms(rooms):
    if not rooms:
        print("No rooms added yet!")
    else:
        print("Room details:")
        for r in rooms:
            print(f"Room Number: {r['room_number']}, Type: {r['Type']}, Price: {r['price']}, Availability: {r['availability']}")

def update_availability(rooms):
    try:
        room_no = int(input("Enter the room number which you want to update: "))
        for r in rooms:
            if r['room_number'] == room_no:
                room_availability = input("Is the room available (yes/no): ").lower()
                r['availability'] = True if room_availability == 'yes' else False
                print("Room availability is updated successfully")
                save_data(rooms, bookings)
                break
        else:
            print("Room number not found")
    except ValueError:
        print("Invalid Input, Please enter Integer value")

def delete_room(rooms):
    try:
        room_no = int(input("Enter the room number which you want to delete: "))
        for r in rooms:
            if r['room_number'] == room_no:
                rooms.remove(r)
                print(f"Room no {room_no} is deleted successfully")
                save_data(rooms, bookings)
                return
        print("Room number not found")
    except ValueError:
        print("Invalid Input, Please enter Integer value")
        
def view_feedbacks():
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as file:
            feedback_data = json.load(file)
            if not feedback_data:
                print("No feedbacks available.")
            else:
                print("Customer Feedbacks:")
                for feedback in feedback_data:
                    print(f"Room Number: {feedback['room_number']}, Customer: {feedback['customer_name']}, Feedback: {feedback['feedback']}")
    else:
        print("No feedbacks available.")


def view_available_rooms(rooms):
    available_room = [r for r in rooms if r['availability']]
    if not available_room:
        print("No rooms are currently available")
    else:
        print("Available rooms: ")
        for r in available_room:
            print(f"Room Number: {r['room_number']}, Type: {r['Type']}, Price: {r['price']}")

def book_room(rooms, bookings):
    try:
        view_available_rooms(rooms)
        room_no = int(input("Enter the room number you want to book: "))
        for r in rooms:
            if r['room_number'] == room_no and r['availability']:
                customer_name = input("Enter your name: ")
                customer_phone = input("Enter your phone number: ")

                check_in_date = validate_date(input("Enter check-in date (YYYY-MM-DD): "))
                check_out_date = validate_date(input("Enter check-out date (YYYY-MM-DD): "))

                if not check_in_date or not check_out_date or check_in_date >= check_out_date:
                    print("Invalid dates. Please try again.")
                    return

                bookings.append({
                    "room_number": room_no,
                    "customer_name": customer_name,
                    "customer_phone": customer_phone,
                    "check_in_date": check_in_date.strftime("%Y-%m-%d"),
                    "check_out_date": check_out_date.strftime("%Y-%m-%d"),
                    "feedback": None
                })
                r['availability'] = False
                print("Room booked successfully")
                save_data(rooms, bookings)
                return
        print("Room not available or not found")
    except ValueError:
        print("Invalid Input, Please enter an integer value")

def check_in(rooms, bookings):
    try:
        room_no = int(input("Enter your room number: "))
        for booking in bookings:
            if booking['room_number'] == room_no:
                print(f"Welcome {booking['customer_name']}! Your check-in is confirmed.")
                save_data(rooms, bookings)
                return
        print("Booking not found for this room number.")
    except ValueError:
        print("Invalid Input, Please enter an integer value")

feedback_file = 'feedback.json'

def save_feedback(feedback_entry):
    feedback_data = []
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as file:
            feedback_data = json.load(file)
    feedback_data.append(feedback_entry)
    with open(feedback_file, 'w') as file:
        json.dump(feedback_data, file, indent=4)
    print("Feedback saved successfully.")
    
def check_out(rooms, bookings):
    try:
        room_no = int(input("Enter your room number: "))
        for booking in bookings:
            if booking['room_number'] == room_no:
                feedback = input("How was your stay? Leave feedback: ")
                feedback_entry = {
                    "room_number": room_no,
                    "customer_name": booking['customer_name'],
                    "feedback": feedback
                }
                save_feedback(feedback_entry) 
                bookings.remove(booking)
                for r in rooms:
                    if r['room_number'] == room_no:
                        r['availability'] = True
                        break
                print(f"Check-out successful for room {room_no}. Thank you for staying with us.")
                save_data(rooms, bookings)
                return
        print("No booking found for this room number.")
    except ValueError:
        print("Invalid Input, Please enter an integer value")


def view_booked_rooms(bookings):
    if not bookings:
        print("No bookings found.")
    else:
        name = input("Enter your name: ").lower()
        found = False  
        for b in bookings:
            if b['customer_name'].lower() == name:  
                print(f"Room Number: {b['room_number']}, Name: {b['customer_name']}, Check-In: {b['check_in_date']}, Check-Out: {b['check_out_date']}")
                found = True
        if not found:
            print("No booking found against your name.")


def admin_menu(rooms):
    print("Admin Menu")
    while True:
        try:
            print("\n1. Add room \n2. View rooms \n3. Update availability \n4. Delete room \n5. View Feedbacks \n6. Exit")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_room(rooms)
            elif choice == 2:
                view_rooms(rooms)
            elif choice == 3:
                update_availability(rooms)
            elif choice == 4:
                delete_room(rooms)
            elif choice == 5:
                view_feedbacks()  
            elif choice == 6:
                print("Exiting program. Thank you!")
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Invalid Input, Please enter Integer value")

def customer_menu(rooms, bookings):
    print("Customer Menu")

    while True:
        try:
            print("\n1. View Available rooms \n2. Book a room \n3. Check In \n4. Check out \n5. View My Bookings \n6. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                view_available_rooms(rooms)
            elif choice == 2:
                book_room(rooms, bookings)
            elif choice == 3:
                check_in(rooms, bookings)
            elif choice == 4:
                check_out(rooms, bookings)
            elif choice == 5:
                view_booked_rooms(bookings)
            elif choice == 6:
                break
            else:
                print("Invalid Choice, Please try again")
        except ValueError:
            print("Invalid Input, Please enter Integer value")

def main():
    display_title()
    rooms, bookings = load_data()  
    
    print("Welcome to Hotel Management System")
    print("Are you an Admin or a Customer?")
    role = input("Enter your role (Admin/Customer): ").strip().lower()

    if role == 'admin':
        admin_menu(rooms)  
    elif role == 'customer':
        customer_menu(rooms, bookings)  
    else:
        print("Invalid Role. Exiting...")
        
if __name__ == "__main__":
    main()
