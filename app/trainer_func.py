from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from models.enums import AvailabilityType
from models.trainer import Trainer
from models.member import Member
from app.member_func import view_member_health_metrics, view_member_fitness_goals
from models.trainer_availability import TrainerAvailability

from app.schedule import DOW, getInputtedDate, getInputtedDates, getInputtedHours, getAdhocSchedule, getRecurringSchedule, getAssignedClasses

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
                print(f"\nLogin Successfully. Welcome {trainer.name}!")
                menu(engine, trainer)
            else:
                print("Trainer not found. Please enter correct email or contact your admin.")
            
        except Exception as e:
            print(f"Error: {e}")

def menu(engine, trainer):
    logged_in = True if trainer else False
    while logged_in:
        print(f"""\n=== {trainer.name} Trainer Dashboard ===\n1. Set Availability\n2. Schedule View\n3. Member Lookup\n4. Logout""")

        choice = input("Select an option: ")
        if choice == '1':
            setAvailability(engine, trainer)
        elif choice == '2':
            viewSchedule(engine, trainer)
        elif choice == '3':
            lookupMember(engine, trainer)
        elif choice == '4':
            logged_in = False
        else:
            print("Invalid option. Please try again.")

def setAvailability(engine, trainer):
    while True:
        print(f"""
=== Update Trainer Availability for {trainer.name} ===
1. Update Recurring (Weekly) Schedule
2. Submit Adhoc (One Time) Schedule
3. View Availability Schedule
4. Return to Trainer Menu
""")
        choice = input("Select an option: ")
        if choice == '1':
            updateRecurringSchedule(engine, trainer)
        elif choice == '2':
            submitAdhocTime(engine, trainer)
        elif choice == '3':
            viewAvailabilitySchedule(engine, trainer)
        elif choice == '4':
            break
        else:
            print(f'Invalid Input: {choice}')

# trainer: Trainer
def updateRecurringSchedule(engine, trainer):
    ranges = []
    for i in range(len(DOW)):
        while True:
            try:
                print('\nFor each day of the week, please input hours for the selected day of the week in the following format "HH:MM,HH:MM"')
                print('If you are not available for that day of the week, please enter "NA".')
                print('To exit, enter "back".\n')
                hours = input(f'Please enter your availability for {DOW[i]}: ').strip()

                if hours.lower() == 'back':
                    print('Exiting Recurring Trainer Schedule Manager')
                    return
                else:
                    tsr = getInputtedHours(hours, datetime(1996, 1, i+1))
                    if not tsr:
                        continue

                ranges.append(TrainerAvailability(
                    trainer_email=trainer.email,
                    time_stamp_range=tsr,
                    availability_type=AvailabilityType.RECURRING
                ))
                
                break
            except Exception as e:
                print(f'Invalid Input: {hours}')

    with Session(engine) as session:
        session.query(TrainerAvailability).filter_by(
            trainer_email=trainer.email,
            availability_type=AvailabilityType.RECURRING
        ).delete()
        
        session.add_all(ranges)
        session.commit()
        print('Updated Recurring Schedule')

# trainer: Trainer
def submitAdhocTime(engine, trainer):
    while True:
        try: 
            print('To exit, enter "back".')
            inp = input('Please enter the date you\'d like to overwrite. (YYYY-MM-DD)').strip()
            if inp.lower() == 'back':
                return
            date = getInputtedDate(inp)
            if date:
                break
        except Exception as e:
            print(e)

    time_ranges = []
    while True:
        try:
            print('\nIf you\'d like to work multiple time periods on the same day, you must enter two even if it would be during your expected hours')
            print('For example, if have an appointment from 10-12 and you normally work 8-4, you\'d have to enter 8-10 and 12-4')
            print('If you are taking the entire day off, please enter "NA"')
            print('To submit, enter "submit"')
            print('To exit, enter "back".\n')
            time_str = input('Please enter the time you\'d like to update. "HH:MM,HH:MM"').strip()
            if time_str.lower() == 'back':
                return
            elif time_str.lower() == 'submit':
                break

            tsr = getInputtedHours(time_str, date)
            if not tsr:
                continue
            time_ranges.append(TrainerAvailability(
                trainer_email=trainer.email,
                time_stamp_range=tsr,
                availability_type=AvailabilityType.ADHOC
            ))
            
        except Exception as e:
            print(e)
    
    try:
        with Session(engine) as session:
            session.add_all(time_ranges)
            session.commit()
            print(f'Added Adhoc Availability')
    except:
        print('Error Updating Schedule, please check that you do not have a previous schedule set')

#trainer Trainer
def viewAvailabilitySchedule(engine, trainer):
    while True:
        print('=== View Schedule ===')
        print('1. View Recurring Schedule')
        print('2. View Schedule over Time Period')
        print('3. Back')
        choice = input('Please select an option: ')
        if choice == '1':
            viewRecurringSchedule(engine, trainer)
        elif choice == '2':
            while True: 
                inp = input('Please input the date range you\'d like to view in the format "YYYY-MM-DD,YYYY-MM-DD": ')
                tsr = getInputtedDates(inp)
                if tsr:
                    break
            viewAdhocSchedule(engine, trainer, tsr)
        elif choice == '3':
            return

# trainer: Trainer
def viewRecurringSchedule(engine, trainer):    
    rSched = getRecurringSchedule(engine, trainer)
    print(f"=== {trainer.name}'s Weekly Schedule ===")
    for day in rSched:
        print(f"{day['dow']:10} {day['start']} - {day['end']}")

# trainer: Trainer
# time_range: DateTimeRange of Dates with no Time
def viewAdhocSchedule(engine, trainer, time_range):
    aSched = getAdhocSchedule(engine, trainer, time_range)
    print(f"==={trainer.name}'s Schedule from {time_range.lower.date()} to {time_range.upper.date()} ===")
    for day in aSched:
        print(f"\n=== {day['dow']:10} {day['date']} ===")
        for timeslot in day['hours']:
            print(f"{timeslot['start']} to {timeslot['end']}")

def viewSchedule(engine, trainer):
    while True: 
        inp = input('Please input the date range you\'d like to view in the format "YYYY-MM-DD,YYYY-MM-DD": ')
        tsr = getInputtedDates(inp)
        if tsr:
            break

    results = getAssignedClasses(engine, trainer, tsr)
    if not results:
        print('No Assigned Classes during Time Slot entered')
        return

    print('[P(ID)] Personal Training Session | [G(ID)] Group Fitness Class')
    print(f'=== {trainer.name}\'s Schedule ===')
    for result in results:
        class_type = result.type
        class_id = result.id
        dow = result.time_stamp_range.lower.strftime('%A')
        date = result.time_stamp_range.lower.strftime('%Y-%m-%d')
        start_time = result.time_stamp_range.lower.strftime('%H:%M')
        end_time = result.time_stamp_range.upper.strftime('%H:%M')
        room = result.room_id
        print(f'[{class_type}{class_id}] {dow} {date} @ {start_time} to {end_time} in Room {room}')

def lookupMember(engine, trainer):
    input_name = input("Name of Member: ")
    with Session(engine) as session:
        searched_member = session.query(Member).filter(func.lower(Member.name) == func.lower(input_name)).all()
        for member in searched_member:
            view_member_fitness_goals(engine, member.email)
            view_member_health_metrics(engine, member.email)
        