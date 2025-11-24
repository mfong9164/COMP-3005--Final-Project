from sqlalchemy.orm import Session
from models.trainer import Trainer

MENU = """
=== Trainer Dashboard ===
1. Set Availability
2. Schedule View
3. Member Lookup
4. Logout
"""

def login(engine):
    login = input("Enter your email: ")
    with Session(engine) as session:
        try:
            trainer = session.query(Trainer).filter_by(email=login).first()
            if trainer:
                print(f"Login Successfully. Welcome {trainer.name}!")
                menu(engine, trainer)
            else:
                print("Trainer not found. Please enter correct email or contact your admin.")
            
        except Exception as e:
            print(f"Error: {e}")

def menu(engine, trainer):
    logged_in = True if trainer else False
    while logged_in:
        print(MENU)
        choice = input("Select an option: ")
        
        if choice == '1':
            setAvailability(engine, trainer)
        elif choice == '2':
            viewSchedule(engine, trainer)
        elif choice == '3':
            lookupMember(engine, trainer)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

def setAvailability(engine, trainer):
    pass

def viewSchedule(engine, trainer):
    pass

def lookupMember(engine, trainer):
    pass