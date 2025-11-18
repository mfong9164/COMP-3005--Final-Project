from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from models.member import Member
from models.health_metric import HealthMetric
from models.fitness_goal import FitnessGoal
from models.room import Room
from models.admin_staff import AdminStaff
from models.trainer_availability import TrainerAvailability
from models.bill import Bill
from models.group_fitness_bill import GroupFitnessBill
from models.personal_training_bill import PersonalTrainingBill

DB_USER = 'postgres'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'Health and Fitness Club Management System'

def create_connection():
    try:
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        with engine.connect() as conn:
            print("Connected")
            Base.metadata.create_all(engine, checkfirst=True)
    except Exception as e:
        print(f"Failed: {e}")
        return

    with Session(engine) as session:
        pass

if __name__ == '__main__':
    create_connection()
    
