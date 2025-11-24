from sqlalchemy.orm import Session
from sqlalchemy import select
from models.member import Member
from models.trainer import Trainer
from models.admin import Admin

def main_menu(engine):
    # main menu to select user role
    while True:
        print("\n=== Health & Fitness Club Management System ===")
        print("1. Member")
        print("2. Trainer")
        print("3. Admin")
        print("4. Exit")
        
        choice = input("Select option: ")
        
        if choice == "1":
            member_menu(engine)
        elif choice == "2":
            trainer_menu(engine)
        elif choice == "3":
            admin_menu(engine)
        elif choice == "4":
            break


def member_menu(engine):

    while True:
        print("\n=== Member Menu ===")
        print("1. Member Login")
        print("2. Member Registration")
        print("3. Back to Main Menu")
        
        choice = input("Select option: ")
        
        if choice == "1":
            member_login(engine)

        elif choice == "2":
            member_registration(engine)

        elif choice == "3":
            break  # Go back to main menu
        else:
            print("Invalid option. Please try again.")


def member_login(engine):
    member_email = input("Enter your email: ")

    with Session(engine) as session:
        try:
            member = session.query(Member).filter_by(email=member_email).first()

            if member:
                print(f"Login Successfully. Welcome {member.name}!")
                member_dashboard(engine, member_email)
            
            else:
                print("Member not found. Please enter correct email or register.")
            
        except Exception as e:
            print(f"Error: {e}")

def member_dashboard(engine, member_email):
    # member dashboard
    while True:

        ## add more if needed
        print("\n=== Member Dashboard ===")
        print("1. Update Personal Details")
        print("2. Update Health History")
        print("3. Update Fitness Goals")
        print("4. Logout")
        
        choice = input("Select option: ")
        
        if choice == "1":
            update_member_profile(engine, member_email)
        elif choice == "2":
            log_member_health_metrics(engine, member_email)
        elif choice == "3":
            pass
        elif choice == "4":
            print("Logged out. Returning to Member Menu...")
            break  # Goes back to member_menu
        else:
            print("Invalid option. Please try again.")

def update_member_profile(engine, member_email):
    pass

def log_member_health_metrics(engine, member_email):
    pass

def trainer_menu(engine):
    # trainer UI code here
    pass

def admin_menu(engine):
    # admin UI code here
    pass