from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
import sys
from pathlib import Path
from getpass import getpass

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from models.admin import Admin
from models.bill import Bill
from models.fitness_goal import FitnessGoal
from models.group_fitness_bill import GroupFitnessBill
from models.group_fitness_class import GroupFitnessClass
from models.health_metric import HealthMetric
from models.member import Member
from models.personal_training_bill import PersonalTrainingBill
from models.personal_training_session import PersonalTrainingSession
from models.room import Room
from models.trainer_availability import TrainerAvailability
from models.trainer import Trainer
from models.equipment import Equipment
from models.maintenance_ticket import MaintenanceTicket
from models.participates_in import ParticipatesIn
from app.sample_data import getSampleData
from models.paid_date_trigger import create_paid_date_trigger
from models.availability_triggers import create_init_trainer_availability_trigger, check_class_time_trigger
from models.unpaid_bills_view import create_unpaid_bills_view, drop_unpaid_bills_view

from app.member_func import member_menu
from app.trainer_func import login as trainer_menu
from app.admin_func import login as admin_menu

# Database Configuration
DB_USER = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'Health and Fitness Club Management System'


def create_connection():
    try:
        DB_PASSWORD = getpass("DB Password: ")
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

        with engine.connect() as conn:
            print("Connected")

            drop_unpaid_bills_view(engine)
            add_btre_gist(conn)

            Base.metadata.drop_all(engine, checkfirst=True)            
            Base.metadata.create_all(engine, checkfirst=True)

            # we create the trigger after tables are created
            create_paid_date_trigger(engine)

            # create the view after tables are created
            create_unpaid_bills_view(engine)
            
            create_init_trainer_availability_trigger(engine)

            check_class_time_trigger(engine)

    except Exception as e:
        print(f"Failed: {e}")
        quit()

    with Session(engine) as session:
        try:
            pass
            sample_data = getSampleData()
            session.add_all(sample_data)
            session.commit()
            
        except Exception as e:
            print(f"Failed: {e}")
            quit()
    
    return engine

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
        else:
            print("Invalid option. Please try again.")

def add_btre_gist(conn):
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist;"))
    conn.commit()
    print("btree_gist extension created successfully.")

if __name__ == '__main__':
    engine = create_connection()
    main_menu(engine)