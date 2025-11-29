import enum

class PaymentMethod(enum.Enum):
    CASH = 0
    DEBIT = 1
    CREDIT = 2

class GoalType(enum.Enum):
    WEIGHT = 0
    BODY_FAT_PERCENTAGE = 1
    CARDIO = 2

class AvailabilityType(enum.Enum):
    RECURRING = 0
    ADHOC = 1

class Gender(enum.Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2

class EquipmentStatus(enum.Enum):
    IN_SERVICE = 0
    OUT_OF_SERVICE = 1