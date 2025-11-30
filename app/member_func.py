from sqlalchemy.orm import Session, joinedload
from models.member import Member
from models.fitness_goal import FitnessGoal
from operator import attrgetter
from models.health_metric import HealthMetric
from models.bill import Bill
from models.group_fitness_bill import GroupFitnessBill
from models.enums import GoalType, PaymentMethod, Gender

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

def member_registration(engine):
    while True:
        with Session(engine) as session:
            try:
                print(f"\n=== Member Registration ===")
                input_email = input("Email: ")
                input_name = input("Name: ")
                input_date_of_birth = input("Date of birth (YYYY-MM-DD): ")
                input_gender = (input("Gender (Male, Female, Other): ").upper())
                input_phone_number = input("Phone Number (##########): ")

                session.add(Member(email=input_email,name=input_name,date_of_birth=input_date_of_birth,gender=input_gender,phone_number=input_phone_number))
                session.commit()
                break
            except Exception as e:
                print(f"Registration Error: {e}")





def member_dashboard(engine, member_email):
    view_member_fitness_goals(engine, member_email)
    view_member_health_metrics(engine, member_email)
    while True:
        with Session(engine) as session:
            try:
                member = session.query(Member).filter_by(email=member_email).first()

                print(f"\n=== {member.name} Dashboard ===")
                print("1. Profile Management")
                print("2. Health & Fitness")
                print("3. Billing & Payments")
                print("4. Group Class Registration")
                print("5. Logout")
                
                choice = input("Select option: ")

                if choice == "1":
                    manageProfile(engine, member_email)
                
                elif choice == "2":
                    manageHealthAndFitness(engine, member_email)
                
                elif choice == "3":
                    manageBilling(engine, member_email)
                
                elif choice == "4":
                    # TODO: Liam's class registration function
                    pass

                elif choice == "5":
                    print("Logged out. Returning to Member Menu.")
                    break

                else:
                    print("Invalid option. Please try again.")  

            except Exception as e:
                print(f"Error: {e}")
        





def manageProfile(engine, member_email):
    # manage personal details section menu
    while True:
        print("\n=== Profile Management ===")
        print("1. View Personal Details")
        print("2. Update Personal Details")
        print("3. Back to Dashboard")
        
        choice = input("Select option: ")
        
        if choice == "1":
            viewPersonalDetails(engine, member_email)
        elif choice == "2":
            update_member_profile(engine, member_email)
        elif choice == "3":
            break
        else:
            print("Invalid option. Please try again.")





def viewPersonalDetails(engine, member_email):
    with Session(engine) as session:
        try:
            member = session.query(Member).filter_by(email=member_email).first()
            
            if member:
                print(f"\n=== Personal Details ===")
                print(f"Name: {member.name}")
                print(f"Email: {member.email}")
                print(f"Date of Birth: {member.date_of_birth}")
                
                # Convert gender enum to string
                gender_string = str(member.gender)
                gender_result = gender_string.split('.')[-1]
                print(f"Gender: {gender_result}")
                
                print(f"Phone Number: {member.phone_number}")
            else:
                print("Member not found.")
                
        except Exception as e:
            print(f"Error: {e}")






def manageHealthAndFitness(engine, member_email):
    while True:
        print("\n=== Health & Fitness ===")
        print("1. View Health Metrics")
        print("2. Add Health Metric")
        print("3. View Fitness Goals")
        print("4. Update Fitness Goals")
        print("5. Back to Dashboard")
        
        choice = input("Select option: ")
        
        if choice == "1":
            view_member_health_metrics(engine, member_email)
        elif choice == "2":
            add_new_member_health_metrics(engine, member_email)
        elif choice == "3":
            view_member_fitness_goals(engine, member_email)
        elif choice == "4":
            update_member_fitness_goals(engine, member_email)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")






def manageBilling(engine, member_email):
    while True:
        print("\n=== Billing & Payments ===")
        print("1. View All My Bills")
        print("2. View Unpaid Bills")
        print("3. Pay Bill")
        print("4. Back to Dashboard")
        
        choice = input("Select option: ")
        
        if choice == "1":
            view_my_bills(engine, member_email)
        elif choice == "2":
            view_my_unpaid_bills(engine, member_email)
        elif choice == "3":
            pay_bill(engine, member_email)
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")






def update_member_profile(engine, member_email):
    with Session(engine) as session:

        member = session.query(Member).filter_by(email=member_email).first()
        try:
            if member:

                # email cannot be changed due to foreign key constraints
                print(f"\nCurrent Email: {member.email}")
                print("Note: Email cannot be changed as it is used as your account identifier.")

                print(f"\nCurrent Name: {member.name}")
                new_name = input("Enter new name (or press Enter to skip): ")
                if new_name:
                    member.name = new_name
                
                # convert the gender enum to a string to display their current gender
                member_gender_string = str(member.gender)
                member_gender_result = member_gender_string.split('.')[-1]
                print(f"\nCurrent Gender: {member_gender_result}")

                new_gender = input("Enter new gender (MALE/FEMALE/OTHER) (or press Enter to skip): ")
                if new_gender:
                    if new_gender.upper() != "MALE" and new_gender.upper() != "FEMALE" and new_gender.upper() != "OTHER":
                        print("Invalid gender. Please enter MALE, FEMALE, or OTHER.")
                        return
                    member.gender = Gender[new_gender.upper()]
                

                print(f"\nCurrent Phone: {member.phone_number}")
                new_phone = input("Enter new phone (or press Enter to skip): ")
                if new_phone:
                    if len(new_phone) != 10 or not new_phone.isdigit():
                        print("Invalid phone number. Please enter a 10 digit phone number.")
                        return

                    member.phone_number = new_phone
                
                session.commit()

                print("Profile updated successfully!")

        except Exception as e:
            print(f"Error: {e}")
            session.rollback()




def add_new_member_health_metrics(engine, member_email):
    try:
        height = float(input("Enter height (cm): "))
        weight = float(input("Enter weight (kg): "))
        heart_rate = int(input("Enter heart rate (bpm): "))
        
        if height <= 0 or weight <= 0 or heart_rate <= 0 or heart_rate > 300:
            print("Invalid input. Please enter valid values.")
            return
        
        with Session(engine) as session:
            new_metric = HealthMetric(member_email=member_email, height=height, weight=weight, heart_rate=heart_rate)
            session.add(new_metric)
            session.commit()
            print("Health metric added successfully!")

    except ValueError:
        print("Invalid input. Please enter numbers.")

    except Exception as e:
        print(f"Error: {e}")






def view_member_health_metrics(engine, member_email):
    with Session(engine) as session:
        member = session.query(Member).filter_by(email=member_email).first()

        if member:
            # LAZY LOADING: health_metrics loads when accessed here with a separate query
            # this is efficient because we only load health metrics if the member exists
            # if member didn't exist, we avoid the extra query to load health metrics
            metrics = member.health_metrics
            if metrics:
                print(f"\n--- {member.name} Latest Health Metrics ---")

                # sort the metrics from newest to oldest and get only the latest 5
                for metric in sorted(metrics, key=attrgetter('created'), reverse=True)[:5]:
                    print(f"\nDate: {metric.created}")
                    print(f"Height: {metric.height} cm")
                    print(f"Weight: {metric.weight} kg")
                    print(f"Heart Rate: {metric.heart_rate} bpm")
            else:
                print("No health metrics found.")







def view_member_fitness_goals(engine, member_email):
    with Session(engine) as session:
        member = session.query(Member).filter_by(email=member_email).first()

        if member:
            fitness_goals = member.fitness_goals
            
            # create a dictionary to map goal_type to amount to lookup if a goal exists/set
            goals_dict = {}
            for goal in fitness_goals:
                goals_dict[goal.goal_type] = goal.amount
            
            print(f"\n--- {member.name} Fitness Goals ---")
            
            if GoalType.WEIGHT in goals_dict:
                print(f"Weight Goal: {goals_dict[GoalType.WEIGHT]} kg")
            else:
                print(f"Weight Goal: N/A")
            
            if GoalType.BODY_FAT_PERCENTAGE in goals_dict:
                print(f"Body Fat Percentage Goal: {goals_dict[GoalType.BODY_FAT_PERCENTAGE]}%")
            else:
                print(f"Body Fat Percentage Goal: N/A")
            
            if GoalType.CARDIO in goals_dict:
                print(f"Cardio Goal: {goals_dict[GoalType.CARDIO]} minutes")
            else:
                print(f"Cardio Goal: N/A")






def update_member_fitness_goals(engine, member_email):
    try:
        print("\n1. Weight Target")
        print("2. Body Fat Percentage Target")
        print("3. Cardio Target")
        goal_type = int(input("Choose a Goal Type to enter: "))

        with Session(engine) as session:
            member = session.query(Member).filter_by(email=member_email).first()

            goal_type_enum = None
            amount = None
            
            if goal_type == 1:
                goal_type_enum = GoalType.WEIGHT
                amount = int(input("Enter weight goal (kg): "))

            elif goal_type == 2:
                goal_type_enum = GoalType.BODY_FAT_PERCENTAGE
                amount = int(input("Enter body fat % goal: "))

            elif goal_type == 3:
                goal_type_enum = GoalType.CARDIO
                amount = int(input("Enter cardio time goal (mins): "))
            else:
                print("Invalid option.")
                return

            # check if goal already exists using relationship
            existing_goal = None
            for goal in member.fitness_goals:
                if goal.goal_type == goal_type_enum:
                    existing_goal = goal
                    break
            
            if existing_goal:
                # update existing goal
                existing_goal.amount = amount
                print(f"Fitness goal updated successfully!")
            else:
                # create the new goal
                new_goal = FitnessGoal(member_email=member_email, goal_type=goal_type_enum, amount=amount)
                session.add(new_goal)
                print(f"Fitness goal added successfully!")
            
            session.commit()

    except ValueError:
        print("Invalid input.")
    
    except Exception as e:
        print(f"Error: {e}")






def view_my_bills(engine, member_email):
    with Session(engine) as session:
        try:
            # EAGER LOADING: using joinedload to load member with bills and nested relationships in fewer queries
            # this loads bills, group_fitness_bills, and fitness_class all at once using JOINs
            # this is more efficient than lazy loading when we know we'll need all the bill data
            member = session.query(Member).options(joinedload(Member.bills).joinedload(Bill.group_fitness_bills).joinedload(GroupFitnessBill.fitness_class)).filter_by(email=member_email).first()
            
            if not member:
                print("Member not found.")
                return
            
            # bills are already loaded from the query above (eager loading), no additional query needed
            bills = member.bills
            
            if not bills:
                print("\nYou have no bills.")
                return
            
            print(f"\n=== Your Bills ===")
            
            # sort the bills from newest to oldest and display them to the user
            for bill in sorted(bills, key=attrgetter('id'), reverse=True):
                print(f"\n{'='*50}")
                print(f"Bill ID: {bill.id}")
                print(f"Amount: ${bill.amount_due:.2f}")
                print(f"Payment Method: {bill.payment_method.name}")
                
                if bill.paid:
                    print(f"Status: PAID")
                    if bill.paid_date:
                        print(f"Paid Date: {bill.paid_date}")
                else:
                    print(f"Status: UNPAID")
                
                # show line items
                print("\nItems on this bill:")
                
                # Calculate total from classes
                classes_total = 0.0
                if bill.group_fitness_bills:
                    for gf_bill in bill.group_fitness_bills:
                        # this goes through each group fitness class bill the member has and accumulates the total price of those bills
                        # it also displays individual group fitness class bills and their prices
                        class_obj = gf_bill.fitness_class
                        classes_total += class_obj.price
                        print(f"  - Group Fitness Class #{class_obj.id} - ${class_obj.price:.2f}")
                
                # calculate membership fee
                membership_amount = bill.amount_due - classes_total
                if membership_amount > 0:
                    print(f"  - Membership Fee - ${membership_amount:.2f}")
                    
        except Exception as e:
            print(f"Error: {e}")






def view_my_unpaid_bills(engine, member_email):
    from sqlalchemy import text
    
    with Session(engine) as session:
        try:
            # Use the unpaid_bills_view and filter by member email
            query = text("""
                SELECT * FROM unpaid_bills_view 
                WHERE member_email = :member_email 
                ORDER BY bill_id DESC
            """)
            
            result = session.execute(query, {"member_email": member_email})
            rows = result.fetchall()
            
            # if no unpaid bills are found for that member, display message
            if not rows:
                print("\nYou have no unpaid bills.")
                return
            
            print(f"\n=== Your Unpaid Bills ===")
            
            total_due = 0.0
            
            # prints each unpaid bill information
            for row in rows:
                print(f"\n{'='*50}")
                print(f"Bill ID: {row.bill_id}")
                print(f"Amount: ${row.amount_due:.2f}")
                print(f"Payment Method: {row.payment_method}")
                print(f"Status: UNPAID")
                
                # get the full Bill object to access the line items
                # EAGER LOADING: load bill with group_fitness_bills and fitness_class to avoid lazy loading queries
                bill = session.query(Bill).options(joinedload(Bill.group_fitness_bills).joinedload(GroupFitnessBill.fitness_class)).filter_by(id=row.bill_id).first()
                
                if bill:
                    # show line items
                    print("\nItems on this bill:")
                    
                    # calculate total from the group fitness classes
                    # group_fitness_bills and fitness_class are already loaded, no additional queries needed
                    classes_total = 0.0
                    if bill.group_fitness_bills:
                        for gf_bill in bill.group_fitness_bills:
                            # this goes through each group fitness class bill the member has and accumulates the total price of those bills
                            # it also displays individual group fitness class bills and their prices
                            class_obj = gf_bill.fitness_class
                            classes_total += class_obj.price
                            print(f"  - Group Fitness Class #{class_obj.id} - ${class_obj.price:.2f}")
                    
                    # calculate membership fee
                    membership_amount = bill.amount_due - classes_total
                    if membership_amount > 0:
                        print(f"  - Membership Fee - ${membership_amount:.2f}")
                
                total_due += row.amount_due
            
            # show total amount due
            print(f"\n{'='*50}")
            print(f"Total Amount Due: ${total_due:.2f}")
                    
        except Exception as e:
            print(f"Error: {e}")





def pay_bill(engine, member_email):
    try:
        bill_id = int(input("Enter bill ID to pay: "))
        
        with Session(engine) as session:
            # find the bill and make sure it belongs to this member
            # EAGER LOADING: load bill with group_fitness_bills and fitness_class to avoid multiple queries
            bill = session.query(Bill).options(joinedload(Bill.group_fitness_bills).joinedload(GroupFitnessBill.fitness_class)).filter_by(id=bill_id, member_email=member_email).first()
            
            if not bill:
                print(f"Bill ID {bill_id} not found or does not belong to you.")
                return
            
            if bill.paid:
                print(f"Bill ID {bill_id} is already paid.")
                if bill.paid_date:
                    print(f"Paid on: {bill.paid_date}")
                return
            
            # show bill details
            print(f"\nBill Details:")
            print(f"Bill ID: {bill.id}")
            print(f"Amount: ${bill.amount_due:.2f}")
            
            # show line items and their prices
            # group_fitness_bills and fitness_class are already loaded, no additional queries needed
            print("\nItems on this bill:")
            classes_total = 0.0
            if bill.group_fitness_bills:
                for gf_bill in bill.group_fitness_bills:
                    class_obj = gf_bill.fitness_class
                    classes_total += class_obj.price
                    print(f"  - Group Fitness Class #{class_obj.id} - ${class_obj.price:.2f}")
            
            # calculate the membership fee
            membership_amount = bill.amount_due - classes_total
            if membership_amount > 0:
                print(f"  - Membership Fee - ${membership_amount:.2f}")
            
            confirm = input("\nPay this bill? (y/n): ").lower().strip()
            
            if confirm == 'y':
                # ask for payment method
                print("\nPayment Method:")
                print("1. Cash")
                print("2. Debit")
                print("3. Credit")
                
                payment_choice = input("Enter choice (1, 2, or 3): ").strip()
                
                if payment_choice == '1':
                    payment_method = PaymentMethod.CASH
                elif payment_choice == '2':
                    payment_method = PaymentMethod.DEBIT
                elif payment_choice == '3':
                    payment_method = PaymentMethod.CREDIT
                else:
                    print("Invalid payment method.")
                    return
                
                # Update the bill with payment method and mark as paid
                bill.payment_method = payment_method
                bill.paid = True
                session.commit()
                
                print(f"\nPayment recorded! Bill ID {bill_id} is now marked as PAID.")
                print(f"Payment Method: {payment_method.name}")
                
                # the trigger will set the paid_date automatically
                session.refresh(bill)  # this refreshes the bill object to get the latest data from the database
                if bill.paid_date:
                    print(f"Payment date: {bill.paid_date}")
            else:
                print("Payment cancelled.")
                
    except ValueError:
        print("Invalid input. Please enter a valid bill ID.")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'session' in locals():
            session.rollback()