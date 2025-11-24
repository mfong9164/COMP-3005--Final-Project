from sqlalchemy.orm import Session
from models.admin import Admin

MENU = """
=== Admin Dashboard ===
1. Room Booking
2. Equipment Maintenance
3. Class Management
4. Billing & Payment
5. Logout
"""

def login(engine):
    login = input("Enter your email: ")
    with Session(engine) as session:
        try:
            admin = session.query(Admin).filter_by(email=login).first()
            if admin:
                print(f"Login Successfully. Welcome {admin.name}!")
                menu(engine, admin)
            else:
                print("Admin not found. Please enter correct email or contact your admin.")
            
        except Exception as e:
            print(f"Error: {e}")

def menu(engine, admin):
    logged_in = True if admin else False
    while logged_in:
        print(MENU)
        choice = input("Select an option: ")
        
        if choice == '1':
            bookRoom(engine, admin)
        elif choice == '2':
            maintainEquipment(engine, admin)
        elif choice == '3':
            manageClasses(engine, admin)
        elif choice == '4':
            manageBilling(engine, admin)
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

def bookRoom(engine, admin):
    pass

def maintainEquipment(engine, admin):
    pass

def manageClasses(engine, admin):
    pass

def manageBilling(engine, admin):
    pass