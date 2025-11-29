from sqlalchemy.orm import Session

from app.schedule import DOW, getInputtedDate, getInputtedHours, getAvailableTrainers, getAvailableRooms

from models.admin import Admin
from models.maintenance_ticket import MaintenanceTicket
from models.equipment import Equipment
from models.enums import EquipmentStatus
from models.enums import PaymentMethod
from models.bill import Bill
from models.group_fitness_bill import GroupFitnessBill
from models.group_fitness_class import GroupFitnessClass
from models.member import Member
from models.participates_in import ParticipatesIn
from models.trainer import Trainer
from models.room import Room

MENU = """
=== Admin Dashboard ===
1. Create Group Fitness Class
2. Manage Maintenance Tickets
3. Billing & Payment
4. Logout
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
        print(f"""\n=== {admin.name} Admin Dashboard ===\n1. Create Group Fitness Class\n2. Manage Maintenance Tickets\n3. Billing & Payment\n4. Logout""")
        choice = input("Select an option: ")
        
        if choice == '1':
            createGroupClass(engine, admin)
        elif choice == '2':
            manageMaintenanceTickets(engine, admin)
        elif choice == '3':
            manageBilling(engine, admin)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

def createGroupClass(engine, admin):
    while True:
        print('Please create a time slot for the class')
        date_str = input('Please enter the date of the class in the format "YYYY-MM-DD": ')
        date = getInputtedDate(date_str)
        if date:
            break
    while True:
        print(f'Date: {date.strftime('%Y-%m-%d')}')
        timeslot_str = input('Please enter the time of the class in the format "HH:MM,HH:MM":')
        tsr = getInputtedHours(timeslot_str, date)
        if tsr:
            break

    trainers = getAvailableTrainers(engine, tsr)
    if len(trainers) == 0:
        print('No available trainers during this time, please select a different time.')
        return
    
    print(f'Available Trainers: {trainers}')
    
    while True:
        trainer_str = input('\n\nPlease select the trainer (case sensitive): ').strip()
        try:
            if trainer_str not in trainers:
                print('Invalid Input')
                continue
        except Exception as e:
            print(e)
            continue
        
        with Session(engine) as session:
            trainer = session.query(Trainer).filter_by(email=trainer_str).first()
            if trainer:
                break

    rooms = getAvailableRooms(engine, tsr)
    if len(rooms) == 0:
        print('No available rooms during this time, please select a different time.')
        return

    print(f'Available Rooms: {rooms}')
    
    while True:
        room_str = input('\n\nPlease select the room (case sensitive): ').strip()

        try:
            if int(room_str) not in rooms:
                print('Invalid Input')
                continue
        except Exception as e:
            print(e)

        with Session(engine) as session:
            room = session.query(Room).filter_by(room_id=room_str).first()
            if room:
                break
    
    while True:
        try:
            cost = float(input('\nPlease enter the cost of the class: '))
            break
        except Exception as e:
            print(e)
    
    while True:
        try:
            cap = int(input('\nPlease enter the capacity of the class: '))
            if cap <= 0 or cap >= 20:
                print('Invalid Input, please enter a capacity between 1 and 20')
                break;
            break
        except Exception as e:
            print(e)

    newGFC = GroupFitnessClass(
        trainer_email=trainer.email,
        room_id=room.room_id,
        time_stamp_range=tsr,
        price=cost,
        capacity=cap
    )

    session.add(newGFC)
    session.commit()

def manageMaintenanceTickets(engine, admin):
    while True:
        print("\n=== Maintenance Tickets Management ===")
        print("1. Log New Maintenance Ticket")
        print("2. View Maintenance Tickets")
        print("3. Update Maintenance Ticket Status")
        print("4. Back to Admin Menu")
        
        choice = input("Select option: ")
        
        if choice == '1':
           logMaintenanceTicket(engine, admin)
        elif choice == '2':
            viewMaintenanceTicket(engine, admin)
        elif choice == '3':
            updateMaintenanceTicketStatus(engine, admin)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")






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
                
                # use the relationship to get equipment and all its tickets
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


def manageBilling(engine, admin):
    while True:
        print("\n=== Billing & Payment Management ===")
        print("1. Create New Bill")
        print("2. View All Bills")
        print("3. Add Items to Existing Bill")
        print("4. View Unpaid Bills")
        print("5. Back to Admin Menu")
        
        choice = input("Select option: ")
        
        if choice == '1':
            createBill(engine, admin)
        elif choice == '2':
            viewAllBills(engine, admin)
        elif choice == '3':
            addItemsToBill(engine, admin)
        elif choice == '4':
            viewUnpaidBills(engine, admin)
        elif choice == '5':
            break
        else:
            print("Invalid option.")






def createBill(engine, admin):
    try:
        member_email = input("Enter member email: ").strip()
        
        with Session(engine) as session:
            # check if member exists
            member = session.query(Member).filter_by(email=member_email).first()
            if not member:
                print(f"Member not found: {member_email}")
                return
            
            # ask what to bill for
            print("\nWhat type of bill?")
            print("1. Membership Fee")
            print("2. Group Fitness Class")
            
            bill_type = input("Enter choice (1 or 2): ").strip()
            
            # calculate the amount
            total_amount = 0.0
            
            if bill_type == '1':
                # for the membership fee, just enter the amount
                amount = float(input("Enter membership fee amount: $"))
                if amount < 0:
                    print("Amount cannot be negative.")
                    return
                total_amount = amount
                item_type = "membership"
                
            elif bill_type == '2':
                # group fitness class bill
                class_id = int(input("Enter group fitness class ID: "))
                fitness_class = session.query(GroupFitnessClass).filter_by(id=class_id).first()
                
                if not fitness_class:
                    print(f"Class ID {class_id} not found.")
                    return
                
                # check if the member is enrolled using the relationship
                # The index on class_id will help with this query
                participation = session.query(ParticipatesIn).filter_by(member_email=member_email, class_id=class_id).first()
                
                if not participation:
                    print("Member is not enrolled in this class.")
                    return
                
                # check if already billed for that class using relationship
                already_billed = any(gfb.bill.member_email == member_email for gfb in fitness_class.group_fitness_bills)
                
                if already_billed:
                    print("This class is already billed for this member.")
                    return
                
                total_amount = fitness_class.price
                item_type = "class"
                item_id = class_id
                
            else:
                print("Invalid choice.")
                return
            
            # create the bill
            new_bill = Bill(member_email=member_email, admin_email=admin.email, amount_due=total_amount, payment_method=PaymentMethod.CASH, paid=False)
            session.add(new_bill)
            session.flush()  # this gets us the bill ID
            
            # link the bill to the groupFitnessBill to the bill 
            if item_type == "class":
                gf_bill = GroupFitnessBill(bill_id=new_bill.id, class_id=item_id)
                session.add(gf_bill)
            
            session.commit()
            print(f"\nBill created successfully!")
            print(f"Bill ID: {new_bill.id}")
            print(f"Amount: ${total_amount:.2f}")
            print("Note: Member will select payment method when paying.")
            
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")
        if 'session' in locals():
            session.rollback()





def viewAllBills(engine, admin):
    with Session(engine) as session:
        try:
            bills = session.query(Bill).order_by(Bill.id.desc()).all()
            
            if not bills:
                print("No bills found.")
                return
            
            print("\n=== All Bills ===")
            
            for bill in bills:
                print(f"\n{'='*50}")
                print(f"Bill ID: {bill.id}")
                print(f"Member: {bill.member.name} ({bill.member_email})")
                print(f"Amount: ${bill.amount_due:.2f}")
                print(f"Payment Method: {bill.payment_method.name}")
                
                if bill.paid:
                    print(f"Status: PAID")
                    if bill.paid_date:
                        print(f"Paid Date: {bill.paid_date}")
                else:
                    print(f"Status: UNPAID")
                
                # show what's on the bill (line items)
                print("\nItems on this bill:")
                
                # calculate total from classes
                classes_total = 0.0
                if bill.group_fitness_bills:
                    for gf_bill in bill.group_fitness_bills:
                        class_obj = gf_bill.fitness_class
                        classes_total += class_obj.price
                        print(f"  - Group Fitness Class #{class_obj.id} - ${class_obj.price:.2f}")
                
                # calculate membership fee which is the difference between total and classes
                membership_amount = bill.amount_due - classes_total
                if membership_amount > 0:
                    print(f"  - Membership Fee - ${membership_amount:.2f}")
                    
        except Exception as e:
            print(f"Error: {e}")






def addItemsToBill(engine, admin):
    try:
        bill_id = int(input("Enter bill ID to add items to: "))
        
        with Session(engine) as session:
            # find the bill
            bill = session.query(Bill).filter_by(id=bill_id).first()
            
            if not bill:
                print(f"Bill ID {bill_id} not found.")
                return
            
            # can't add to a paid bill
            if bill.paid:
                print("Cannot add items to a paid bill. Create a new bill instead.")
                return
            
            # calculate current class total to check if membership fee already exists
            classes_total = 0.0
            if bill.group_fitness_bills:
                for gf_bill in bill.group_fitness_bills:
                    classes_total += gf_bill.fitness_class.price
            
            # check if membership fee already exists (if amount > class total)
            has_membership = bill.amount_due > classes_total
            
            print(f"\nCurrent bill amount: ${bill.amount_due:.2f}")
            
            # show menu based on whether membership already exists
            if has_membership:
                print("\nThis bill already includes a membership fee.")
                print("You can add:")
                print("1. Group Fitness Class")
                choice = input("Enter choice (1): ").strip()
            else:
                print("\nWhat would you like to add?")
                print("1. Membership Fee")
                print("2. Group Fitness Class")
                choice = input("Enter choice (1 or 2): ").strip()
            
            if choice == '1':
                if has_membership:
                    print("This bill already has a membership fee. Adding a class instead...")
                    choice = '2'  # switch to adding a class instead
                else:
                    # add membership fee
                    amount = float(input("Enter membership fee amount to add: $"))
                    if amount < 0:
                        print("Amount cannot be negative.")
                        return
                    
                    # update the bill amount
                    bill.amount_due = bill.amount_due + amount
                    
                    session.commit()
                    print(f"Membership fee added to bill.")
                    print(f"New bill amount: ${bill.amount_due:.2f}")
                    return
            
            if choice == '2' or (choice == '1' and has_membership):
                # add a group fitness class
                class_id = int(input("Enter class ID to add: "))
                fitness_class = session.query(GroupFitnessClass).filter_by(id=class_id).first()
                
                if not fitness_class:
                    print(f"Class ID {class_id} not found.")
                    return
                
                # check if member is enrolled using relationship and index
                participation = session.query(ParticipatesIn).filter_by(member_email=bill.member_email, class_id=class_id).first()
                
                if not participation:
                    print("Member is not enrolled in this class.")
                    return
                
                # check if already billed using relationship
                already_billed = any(gfb.bill.member_email == bill.member_email for gfb in fitness_class.group_fitness_bills)
                
                if already_billed:
                    print("This class is already billed for this member.")
                    return
                
                # add it to the bill
                gf_bill = GroupFitnessBill(bill_id=bill.id, class_id=class_id)
                session.add(gf_bill)
                
                # update the bill amount
                bill.amount_due = bill.amount_due + fitness_class.price
                
                session.commit()
                print(f"Class added to bill.")
                print(f"New bill amount: ${bill.amount_due:.2f}")
            
            else:
                print("Invalid choice.")
                
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")
        if 'session' in locals():
            session.rollback()





def viewUnpaidBills(engine, admin):
    from sqlalchemy import text
    
    with Session(engine) as session:
        try:
            # use the view we created called unpaid_bills_view
            result = session.execute(text("SELECT * FROM unpaid_bills_view ORDER BY bill_id DESC"))
            rows = result.fetchall()
            
            if not rows:
                print("\nNo unpaid bills found.")
                return
            
            print("\n=== Unpaid Bills ===")
            
            for row in rows:
                print(f"\n{'='*50}")
                print(f"Bill ID: {row.bill_id}")
                print(f"Member: {row.member_name} ({row.member_email})")
                print(f"Phone: {row.member_phone}")
                print(f"Amount: ${row.amount_due:.2f}")
                print(f"Payment Method: {row.payment_method}")
                print(f"Created by: {row.admin_name}")
                    
        except Exception as e:
            print(f"Error: {e}")