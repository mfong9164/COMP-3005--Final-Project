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
    pass

def member_dashboard(engine, member_email):
    # member dashboard
    
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
        print("4. Update Health Metrics")
        print("5. View Fitness Goals")
        print("6. Update Fitness Goals")
        print("7. Logout")
        
        choice = input("Select option: ")

        if choice == "1":
            # TODO: Liam's Member Dashboard Function
            pass
        
        elif choice == "2":
            update_member_profile(engine, member_email)

        elif choice == "3":
            view_member_health_metrics(engine, member_email)

        elif choice == "4":
            update_member_health_metrics(engine, member_email)
        
        elif choice == "5":
            view_member_fitness_goals(engine, member_email)
        
        elif choice == "6":
            update_member_fitness_goals(engine, member_email)

        elif choice == "7":
            print("Logged out. Returning to Member Menu.")
            break  # Goes back to member_menu

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

            print(f"\nCurrent Gender: {member.gender}")
            new_gender = input("Enter new gender (MALE/FEMALE) (or press Enter to skip): ")
            if new_gender:
                member.gender = new_gender

            print(f"\nCurrent Phone: {member.phone_number}")
            new_phone = input("Enter new phone (or press Enter to skip): ")
            if new_phone:
                member.phone_number = new_phone
            
            session.commit()

            print("Profile updated successfully!")

def update_member_health_metrics(engine, member_email):
    try:
        height = float(input("Enter height (cm): "))
        weight = float(input("Enter weight (kg): "))
        heart_rate = int(input("Enter heart rate (bpm): "))
        
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
                    print(f"{goal.goal_type}: {goal.amount}")
            else:
                print("No fitness goals found.")

def update_member_fitness_goals(engine, member_email):
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

            session.add(new_goal)
            session.commit()
            print("Fitness goal added successfully!")

    except ValueError:
        print("Invalid input.")