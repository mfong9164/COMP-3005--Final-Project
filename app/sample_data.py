from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy.dialects.postgresql import TSRANGE
from psycopg2.extras import DateTimeRange

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

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
from models.enums import *
from datetime import date

def getSampleData():
    data = []
    data += adminSample()
    data += trainerSample()
    data += memberSample()
    data += roomSample()
    data += equipmentSample()
    data += groupFitnessClassSample()  
    data += participatesInSample()
    data += personalTrainingSessionSample()
    return data

def adminSample():
    return [
        Admin (
            email="JamesSmith@gmail.com",
            name="James Smith"
        ), Admin (
            email="ChristopherAnderson@gmail.com",
            name="Christopher Anderson"
        ), Admin (
            email="RonaldClark@gmail.com",
            name="Ronald Clark"
        ), Admin (
            email="MaryWright@gmail.com",
            name="Mary Wright"
        ), Admin (
            email="LisaMitchell@gmail.com",
            name="Lisa Mitchell"
        )
    ]
def trainerSample():
    return [
        Trainer (
            email="MichelleJohnson@gmail.com",
            name="Michelle Johnson",
            gender=Gender.FEMALE
        ), Trainer (
            email="JohnThomas@gmail.com",
            name="John Thomas",
            gender=Gender.MALE
        ), Trainer (
            email="DanielRodriguez@gmail.com",
            name="Daniel Rodriguez",
            gender=Gender.MALE
        ), Trainer (
            email="AnthonyLopez@gmail.com",
            name="Anthony Lopez",
            gender=Gender.MALE
        ), Trainer (
            email="PatriciaPerez@gmail.com",
            name="Patricia Perez",
            gender=Gender.FEMALE
        )
    ]
def memberSample():
    return [
        Member (
            email="NancyWilliams@hotmail.com",
            name="Nancy Williams",
            date_of_birth=date(1975, 2, 11),
            gender=Gender.FEMALE,
            phone_number="5386339149"
        ), Member (
            email="LauraJackson@hotmail.com",
            name="Laura Jackson",
            date_of_birth=date(1975, 3, 12),
            gender=Gender.FEMALE,
            phone_number="2453751180"
        ), Member (
            email="RobertLewis@hotmail.com",
            name="Robert Lewis",
            date_of_birth=date(1975, 4, 13),
            gender=Gender.MALE,
            phone_number="6758939155"
        ), Member (
            email="PaulHill@hotmail.com",
            name="Paul Hill",
            date_of_birth=date(1975, 5, 14),
            gender=Gender.MALE,
            phone_number="2569752330"
        ), Member (
            email="KevinRoberts@hotmail.com",
            name="Kevin Roberts",
            date_of_birth=date(1975, 6, 14),
            gender=Gender.MALE,
            phone_number="6763651789"
        )
    ]
def roomSample():
    return [Room (), Room (), Room (), Room (), Room ()]
def equipmentSample():
    return [
        Equipment (
            name="Bench",
            room_id=4,
            status=EquipmentStatus.IN_SERVICE
        ), Equipment (
            name="Squat Rack",
            room_id=5,
            status=EquipmentStatus.IN_SERVICE
        ), Equipment (
            name="Treadmill",
            room_id=1,
            status=EquipmentStatus.IN_SERVICE
        ), Equipment (
            name="Treadmill",
            room_id=1,
            status=EquipmentStatus.IN_SERVICE
        ), Equipment (
            name="Mat",
            room_id=2,
            status=EquipmentStatus.IN_SERVICE
        )
    ]

def groupFitnessClassSample():
    return [
        GroupFitnessClass(
            trainer_email="PatriciaPerez@gmail.com",
            room_id=1,
            time_stamp_range=DateTimeRange(
                datetime(2024, 12, 20, 9, 0, 0),
                datetime(2024, 12, 20, 10, 0, 0)
            ),
            price=25.00,
            capacity=10
        ),
        GroupFitnessClass(
            trainer_email="MichelleJohnson@gmail.com",
            room_id=2, 
            time_stamp_range=DateTimeRange(
                datetime(2024, 12, 23, 12, 0, 0),
                datetime(2024, 12, 23, 13, 0, 0)
            ),
            price=30.00,
            capacity=6
        ),
        GroupFitnessClass(
            trainer_email="JohnThomas@gmail.com",
            room_id=3,
            time_stamp_range=DateTimeRange(
                datetime(2024, 12, 23, 12, 0, 0),
                datetime(2024, 12, 23, 13, 0, 0)
            ),
            price=20.00,
            capacity=20
        ),
        GroupFitnessClass(
            trainer_email="DanielRodriguez@gmail.com",
            room_id=1,
            time_stamp_range=DateTimeRange(
                datetime(2024, 12, 23, 10, 0, 0),
                datetime(2024, 12, 23, 11, 0, 0)
            ),
            price=35.00,
            capacity=10
        ),
        GroupFitnessClass(
            trainer_email="PatriciaPerez@gmail.com",
            room_id=3,
            time_stamp_range=DateTimeRange(
                datetime(2024, 12, 24, 10, 0, 0),
                datetime(2024, 12, 24, 11, 0, 0)
            ),
            price=25.00,
            capacity=20
        )
    ]

def participatesInSample():
    return [
        ParticipatesIn(
            member_email="NancyWilliams@hotmail.com",
            class_id=1
        ),
        ParticipatesIn(
            member_email="LauraJackson@hotmail.com",
            class_id=1
        ),
        ParticipatesIn(
            member_email="RobertLewis@hotmail.com",
            class_id=1
        ),
        ParticipatesIn(
            member_email="NancyWilliams@hotmail.com",
            class_id=2
        ),
        ParticipatesIn(
            member_email="PaulHill@hotmail.com",
            class_id=2
        ),
        ParticipatesIn(
            member_email="KevinRoberts@hotmail.com",
            class_id=3
        ),
        ParticipatesIn(
            member_email="LauraJackson@hotmail.com",
            class_id=3
        ),
        ParticipatesIn(
            member_email="RobertLewis@hotmail.com",
            class_id=4 
        ),
        ParticipatesIn(
            member_email="PaulHill@hotmail.com",
            class_id=5
        ),
        ParticipatesIn(
            member_email="KevinRoberts@hotmail.com",
            class_id=5
        )
    ]

def personalTrainingSessionSample():
    return [
        PersonalTrainingSession(
            trainer_email="MichelleJohnson@gmail.com",
            member_email="NancyWilliams@hotmail.com",
            room_id=2,
            time_stamp_range=DateTimeRange(datetime(2024, 12, 18, 9, 0, 0),  datetime(2024, 12, 18, 10, 0, 0)),
            price=65.00
        ),
        PersonalTrainingSession(
            trainer_email="JohnThomas@gmail.com",
            member_email="PaulHill@hotmail.com",
            room_id=4,
            time_stamp_range=DateTimeRange(datetime(2024, 12, 19, 15, 0, 0), datetime(2024, 12, 19, 16, 0, 0)),
            price=70.00
        ),
        PersonalTrainingSession(
            trainer_email="DanielRodriguez@gmail.com",
            member_email="KevinRoberts@hotmail.com",
            room_id=3,
            time_stamp_range=DateTimeRange(datetime(2024, 12, 20, 9, 30, 0), datetime(2024, 12, 20, 10, 30, 0)),
            price=60.00
        ),
        PersonalTrainingSession(
            trainer_email="AnthonyLopez@gmail.com",
            member_email="LauraJackson@hotmail.com",
            room_id=5,
            time_stamp_range=DateTimeRange(datetime(2024, 12, 23, 14, 0, 0), datetime(2024, 12, 23, 15, 0, 0)),
            price=75.00
        ),
        PersonalTrainingSession(
            trainer_email="PatriciaPerez@gmail.com",
            member_email="RobertLewis@hotmail.com",
            room_id=4,
            time_stamp_range=DateTimeRange(datetime(2024, 12, 23, 14, 0, 0), datetime(2024, 12, 23, 15, 0, 0)),
            price=50.00
        ),
    ]    