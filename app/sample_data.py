from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys
from pathlib import Path

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
    return [
        Room (
            room_type=RoomType.STUDIO,
            capacity=10
        ), Room (
            room_type=RoomType.STUDIO,
            capacity=6
        ), Room (
            room_type=RoomType.STUDIO,
            capacity=20
        ), Room (
            room_type=RoomType.TRAINING_ROOM,
            capacity=15
        ), Room (
            room_type=RoomType.TRAINING_ROOM,
            capacity=30
        )
    ]
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
            status=EquipmentStatus.OUT_OF_SERVICE
        ), Equipment (
            name="Mat",
            room_id=2,
            status=EquipmentStatus.IN_SERVICE
        )
    ]