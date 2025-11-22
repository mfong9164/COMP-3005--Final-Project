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


DB_USER = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'Health and Fitness Club Management System'

def create_paid_date_trigger(engine):
    # create the trigger function. only set paid_date if paid changed from False to True. if paid is set back to False, clear the paid_date
    function_sql = """
    CREATE OR REPLACE FUNCTION set_paid_date()
    RETURNS TRIGGER AS $$
    BEGIN
        IF OLD.paid = FALSE AND NEW.paid = TRUE THEN
            NEW.paid_date = CURRENT_DATE;
        END IF;
        
        IF NEW.paid = FALSE THEN
            NEW.paid_date = NULL;
        END IF;
        
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

    ## create the trigger, and drop it if it already exists to prevent errors. Before updating the bill, we will check if
    ## the paid column has changed. if it has, we run the trigger function to set the paid date.
    trigger_sql = """
    DROP TRIGGER IF EXISTS trigger_set_paid_date on "Bill";

    CREATE TRIGGER trigger_set_paid_date
    BEFORE UPDATE ON "Bill"
    FOR EACH ROW
    WHEN (OLD.paid IS DISTINCT FROM NEW.paid)
    EXECUTE FUNCTION set_paid_date();
    """

    with engine.connect() as conn:
        conn.execute(text(function_sql))
        conn.execute(text(trigger_sql))
        conn.commit()
        print("Trigger 'trigger_set_paid_date' created successfully")

def create_connection():
    try:
        DB_PASSWORD = getpass("DB Password: ")
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        with engine.connect() as conn:
            print("Connected")
            Base.metadata.drop_all(engine, checkfirst=True)
            Base.metadata.create_all(engine, checkfirst=True)

            # we create the trigger after tables are created
            create_paid_date_trigger(engine)

    except Exception as e:
        print(f"Failed: {e}")
        quit()

    with Session(engine) as session:
        try:
            sample_data = getSampleData()
            session.add_all(sample_data)
            User_email = input("User Email: ")
            if (session.execute(select(Member.email).where(Member.email == User_email)) == User_email):
                print("member login")
        except Exception as e:
            print(f"Failed: {e}")
            quit()

if __name__ == '__main__':
    create_connection()
    


    
