from sqlalchemy.orm import Session
from models.admin import Admin
from models.maintenance_ticket import MaintenanceTicket
from models.equipment import Equipment
from models.enums import EquipmentStatus

MENU = """
=== Admin Dashboard ===
1. Room Booking
2. Log Maintenance Ticket
3. View Maintenance Tickets
4. Update Maintenance Ticket Status
5. Class Management
6. Billing & Payment
7. Logout
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
            logMaintenanceTicket(engine, admin)
        elif choice == '3':
            viewMaintenanceTicket(engine, admin)
        elif choice == '4':
            updateMaintenanceTicketStatus(engine, admin)
        elif choice == '5':
            manageClasses(engine, admin)
        elif choice == '6':
            manageBilling(engine, admin)
        elif choice == '7':
            break
        else:
            print("Invalid option. Please try again.")

def bookRoom(engine, admin):
    pass

def logMaintenanceTicket(engine, admin):
    try:
        equipment_ID = input("Enter the equipment ID: ")
        equipment_ID = int(equipment_ID)

    except ValueError:
        print("Invalid equipment ID. Please enter a valid number.")
        return
    
    description = input("Enter description of the issue: ").strip()
    
    # make sure description is not empty
    if not description:
        print("Description cannot be empty.")
        return
    
    with Session(engine) as session:
        try:
            equipmentExists = session.query(Equipment).filter_by(equipment_id=equipment_ID).first()

            if equipmentExists:
                # if the equipment exists, then create the ticket and mark it out of service
                maintenance_ticket = MaintenanceTicket(admin_email=admin.email, equipment_id=equipment_ID, description=description)

                session.add(maintenance_ticket)
                equipmentExists.status = EquipmentStatus.OUT_OF_SERVICE
                session.commit()

                print("Maintenance ticket logged successfully.")
            
            else:
                print(f"No equipment exists with ID {equipment_ID}.")
                
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()

def viewMaintenanceTicket(engine, admin):
    with Session(engine) as session:
        try:
            tickets = session.query(MaintenanceTicket).all()
            
            if not tickets:
                print("No maintenance tickets found.")
                return
            
            print("\n=== Maintenance Tickets ===")
            for ticket in tickets:
                equipment = ticket.equipment
                status = "Completed" if ticket.completed else "Pending"
                print(f"\nTicket ID: {ticket.id}")
                print(f"Equipment ID: {ticket.equipment_id} - {equipment.name}")
                print(f"Status: {status}")
                print(f"Description: {ticket.description}")
                print(f"Created by: {ticket.admin_email}")
                
        except Exception as e:
            print(f"Error: {e}")

def updateMaintenanceTicketStatus(engine, admin):
    try:
        ticket_id = int(input("Enter the ticket ID to update: "))
    except ValueError:
        print("Invalid ticket ID. Please enter a valid number.")
        return
    
    with Session(engine) as session:
        try:
            ticket = session.query(MaintenanceTicket).filter_by(id=ticket_id).first()
            
            if not ticket:
                print(f"No ticket found with ID {ticket_id}.")
                return
            
            # if ticket has already been completed, then no changes can be made. they must make a new ticket
            if ticket.completed:
                print(f"\nTicket ID {ticket.id} is already completed and cannot be modified.")
                print(f"To report a new issue, please create a new maintenance ticket.")
                return
            
            # show the current ticket information
            print(f"\nTicket ID: {ticket.id}")
            print(f"Equipment ID: {ticket.equipment_id}")
            print(f"Description: {ticket.description}")
            print(f"Current Status: Pending")
            
            mark_complete = input("\nMark this ticket as completed? (y/n): ").lower().strip()
            if mark_complete == 'y':
                ticket.completed = True
                
                # Use the relationship to get equipment and all its tickets
                equipment = ticket.equipment
                all_tickets = equipment.maintenance_tickets
                all_completed = all(t.completed for t in all_tickets)
                
                # if all tickets are completed, set equipment status back to IN_SERVICE
                if all_completed:
                    equipment.status = EquipmentStatus.IN_SERVICE
                    print(f"\nAll maintenance tickets completed for this Equipment. Equipment '{equipment.name}' is now set to IN_SERVICE.")
                
                session.commit()
                print("Ticket marked as completed successfully.")

            else:
                print("No changes made.")
            
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()

def manageClasses(engine, admin):
    pass

def manageBilling(engine, admin):
    pass