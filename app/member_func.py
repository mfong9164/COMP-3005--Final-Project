from sqlalchemy.orm import Session
from models.member import Member
from models.fitness_goal import FitnessGoal
from models.enums import GoalType
from operator import attrgetter
from models.health_metric import HealthMetric

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
    # TODO: Liam's Member Registration Function
    pass

def member_dashboard(engine, member_email):
    while True:

        with Session(engine) as session:
            try:
                member = session.query(Member).filter_by(email=member_email).first()            
            except Exception as e:
                print(f"Error: {e}")
        
        ## add more if needed
        print(f"\n=== {member.name} Dashboard ===")
        print("1. View Personal Details")
        print("2. Update Personal Details")
        print("3. View Health Metrics")
        print("4. Add Health Metric")
        print("5. View Fitness Goals")
        print("6. Add Fitness Goal")
        print("7. Group Class Registration")
        print("8. Logout")
        
        choice = input("Select option: ")

        if choice == "1":
            # TODO: Liam's Member Dashboard Function
            pass
        
        elif choice == "2":
            update_member_profile(engine, member_email)

        elif choice == "3":
            view_member_health_metrics(engine, member_email)

        elif choice == "4":
            add_new_member_health_metrics(engine, member_email)
        
        elif choice == "5":
            view_member_fitness_goals(engine, member_email)
        
        elif choice == "6":
            add_new_member_fitness_goals(engine, member_email)
        
        elif choice == "7":
            # TODO: Liam's class registration function
            pass

        elif choice == "8":
            print("Logged out. Returning to Member Menu.")
            break  # goes back to member_menu

        else:
            print("Invalid option. Please try again.")

def update_member_profile(engine, member_email):
    with Session(engine) as session:
        member = session.query(Member).filter_by(email=member_email).first()

        if member:
            print(f"\nCurrent Email: {member.email}")
            new_email = input("Enter new email (or press Enter to skip): ")
            if new_email:
                member.email = new_email
            
            print(f"\nCurrent Name: {member.name}")
            new_name = input("Enter new name (or press Enter to skip): ")
            if new_name:
                member.name = new_name
            

            member_gender_string = str(member.gender)
            member_gender_result = member_gender_string.split('.')[-1]
            print(f"\nCurrent Gender: {member_gender_result}")
            new_gender = input("Enter new gender (MALE/FEMALE/OTHER) (or press Enter to skip): ")
            if new_gender:
                if new_gender.upper() != "MALE" and new_gender.upper() != "FEMALE" and new_gender.upper() != "OTHER":
                    print("Invalid gender. Please enter MALE, FEMALE, or OTHER.")
                    return
                member.gender = new_gender.upper()
            

            print(f"\nCurrent Phone: {member.phone_number}")
            new_phone = input("Enter new phone (or press Enter to skip): ")
            if new_phone:
                if len(new_phone) != 10 or not new_phone.isdigit():
                    print("Invalid phone number. Please enter a 10 digit phone number.")
                    return

                member.phone_number = new_phone
            
            session.commit()

            print("Profile updated successfully!")

def add_new_member_health_metrics(engine, member_email):
    try:
        height = float(input("Enter height (cm): "))
        weight = float(input("Enter weight (kg): "))
        heart_rate = int(input("Enter heart rate (bpm): "))
        
        if height <= 0 or weight <= 0 or heart_rate <= 0 or heart_rate > 300:
            print("Invalid input. Please enter valid values.")
            return
        
        with Session(engine) as session:
            new_metric = HealthMetric(
                member_email=member_email,
                height=height,
                weight=weight,
                heart_rate=heart_rate
            )
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
            metrics = member.health_metrics
            if metrics:
                print(f"\n--- {member.name} Health Metrics ---")

                # sorts from newest to oldest metrics for a user. this function sorts a list of objects by an attribute
                for metric in sorted(metrics, key=attrgetter('created'), reverse=True):
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
            if fitness_goals:
                print(f"\n--- {member.name} Fitness Goals ---")

                # sorts from newest to oldest fitness_goals for a user. this function sorts a list of objects by an attribute
                for goal in fitness_goals:

                    # by default, the goal_type is an enum object. we need to convert it to a string.
                    goal_type_string = str(goal.goal_type)
                    goal_type_result = goal_type_string.split('.')[-1]

                    print(f"{goal_type_result} Goal: {goal.amount}")
            else:
                print("No fitness goals found.")

def add_new_member_fitness_goals(engine, member_email):
    try:
        print("\n1. Weight")
        print("2. Body Fat Percentage")
        print("3. Cardio")
        goal_type = int(input("Choose a Goal Type to enter: "))

        with Session(engine) as session:
            if goal_type == 1:
                amount = int(input("Enter weight goal: "))
                new_goal = FitnessGoal(member_email=member_email, goal_type=GoalType.WEIGHT, amount=amount)
            if goal_type == 2:
                amount = int(input("Enter body fat % goal: "))
                new_goal = FitnessGoal(member_email=member_email, goal_type=GoalType.BODY_FAT_PERCENTAGE, amount=amount)
            if goal_type == 3:
                amount = int(input("Enter cardio time goal: "))
                new_goal = FitnessGoal(member_email=member_email, goal_type=GoalType.CARDIO, amount=amount)
            else:
                print("Invalid option.")
                return

            session.add(new_goal)
            session.commit()
            print("Fitness goal added successfully!")

    except ValueError:
        print("Invalid input.")
    
    except Exception as e:
        print(f"Error: {e}")