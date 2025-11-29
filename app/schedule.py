from sqlalchemy.orm import Session
from sqlalchemy import literal_column, union_all, func, cast, Time, Date, and_, or_, not_
from psycopg2.extras import DateTimeRange
from datetime import datetime, timedelta

from models.enums import AvailabilityType
from models.trainer import Trainer
from models.trainer_availability import TrainerAvailability
from models.group_fitness_class import GroupFitnessClass
from models.personal_training_session import PersonalTrainingSession
from models.room import Room

# Used for printing Day of Week
DOW = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

# inp str with format "YYYY-MM-DD"
# Returns datetime
def getInputtedDate(inp):
    try:
        date_str = inp.strip().split('-')
        date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        return date
    except Exception as e:
        print(e)

# inp str with format "YYYY-MM-DD,YYYY-MM-DD"
# Returns DateTimeRange
def getInputtedDates(inp):
    try:
        start_str, end_str = inp.strip().split(',')
        start_str = start_str.split('-')
        end_str = end_str.split('-')
        start = datetime(int(start_str[0]), int(start_str[1]), int(start_str[2]))
        end = datetime(int(end_str[0]), int(end_str[1]), int(end_str[2]))
        
        if start >= end:
                print(f'Invalid Date Range: {start.date()} >= {end.date()}')
                return
        
        return DateTimeRange(start, end, '[)')

    except Exception as e:
        print(e)

# inp: string with format: "HH:MM,HH:MM"
# date: timestamprange
# Returns DateTimeRange
def getInputtedHours(inp, date):
    try:
        if inp == 'na':
            start = date
            end = date + timedelta(seconds=1)
            print('Set availability on date to Not Available')
            return DateTimeRange(start, end, '[)')
        else:
            start_str, end_str = inp.strip().split(',')
            start_str = start_str.split(':')
            end_str = end_str.split(':')
            start = date + timedelta(hours=int(start_str[0]), minutes=int(start_str[1]))
            end = date + timedelta(hours=int(end_str[0]), minutes=int(end_str[1]))

            if start < date + timedelta(hours=6) or end > date + timedelta(hours=22):
                print(f'Invalid Time Range: {getTime(start)} {getTime(end)} is outside of gym hours (6:00 to 22:00)')
                return

            if start >= end:
                print(f'Invalid Time Range: {getTime(start)} >= {getTime(end)}')
                return

            if (end - start) < timedelta(hours=1):
                print(f'Invalid Time Range: {getTime(start)} to {getTime(end)} is under 1 hour')
                return

            return DateTimeRange(start, end, '[)')
    except Exception as e:
        print(e)

# Gets Recurring Trainer Availability
# trainer: Trainer
# Returns list of objs: {dow, start, end}
def getRecurringSchedule(engine, trainer):
    with Session(engine) as session:
        results = session.query(TrainerAvailability).filter_by(
            trainer_email=trainer.email,
            availability_type=AvailabilityType.RECURRING
        ).order_by('time_stamp_range').all()

        sched = []
        for result in results:
            sched.append({
                'dow': getDOW(result.time_stamp_range.lower),
                'start': getTime(result.time_stamp_range.lower),
                'end': getTime(result.time_stamp_range.upper)
            })
        
        return sched

# Gets Trainer Availability Schedule over a Date Period
# trainer: Trainer
# time_range: DateTimeRange of 2 Dates (Does NOT consider Time)
# Returns list of objs {date, dow, hours[{start, end}]}
def getAdhocSchedule(engine, trainer, time_range):
    with Session(engine) as session:
        recurring = getRecurringSchedule(engine, trainer)

        sched = []
        current = time_range.lower
        while current <= time_range.upper:
            next = current + timedelta(days=1)
            onDate = DateTimeRange(current, next, '(]')
            results = session.query(TrainerAvailability).filter(
                TrainerAvailability.trainer_email == trainer.email,
                TrainerAvailability.availability_type == AvailabilityType.ADHOC,
                TrainerAvailability.time_stamp_range.op('&&')(onDate)
            ).all()
            
            dow = getDOW(current)
            hours = []
            if results:
                for result in results:
                    hours.append({
                        'start': getTime(result.time_stamp_range.lower),
                        'end': getTime(result.time_stamp_range.upper)
                    })
            else:
                hours.append({
                    'start': recurring[DOW.index(dow)]['start'],
                    'end': recurring[DOW.index(dow)]['end']
                }) 

            sched.append({
                'date': current.date(),
                'dow': dow,
                'hours': hours
            })
            current = next
        return sched

# Gets all Classes Assigned to Trainer
# trainer: Trainer
# tsr: DateTimeRange
def getAssignedClasses(engine, trainer, tsr):
    with Session(engine) as session:
        gfc = session.query(
            GroupFitnessClass.id.label('id'),
            GroupFitnessClass.time_stamp_range.label('time_stamp_range'),
            GroupFitnessClass.room_id.label('room_id'),
            literal_column("'G'").label('type')
        ).filter(
            GroupFitnessClass.trainer == trainer,
            GroupFitnessClass.time_stamp_range.op('&&')(tsr)
        )

        pts = session.query(
            PersonalTrainingSession.id.label('id'),
            PersonalTrainingSession.time_stamp_range.label('time_stamp_range'),
            PersonalTrainingSession.room_id.label('room_id'),
            literal_column("'P'").label('type')
        ).filter(
            PersonalTrainingSession.trainer == trainer,
            PersonalTrainingSession.time_stamp_range.op('&&')(tsr)
        )

        query = union_all(pts, gfc).subquery()
        
        return session.query(
            query.c.id,
            query.c.time_stamp_range,
            query.c.room_id,
            query.c.type
        ).order_by(query.c.time_stamp_range.asc()).all()

# tsr: DateTimeRange *Must be on the same day*
# Returns a list of trainer emails (String)
def getAvailableTrainers(engine, tsr):
    if getDate(tsr.lower) != getDate(tsr.upper):
        print('Invalid TimeStampRange: Different Dates')
        return

    with Session(engine) as session:
        hasOpenAdhoc = session.query(TrainerAvailability).filter(
            TrainerAvailability.trainer_email == Trainer.email,
            TrainerAvailability.time_stamp_range.contains(tsr),
            TrainerAvailability.availability_type == AvailabilityType.ADHOC
        ).exists()

        tsr_date = getDate(tsr.lower)
        hasOtherAdhocOnDate = session.query(TrainerAvailability).filter(
            TrainerAvailability.trainer_email == Trainer.email,
            ~TrainerAvailability.time_stamp_range.contains(tsr),
            cast(func.lower(TrainerAvailability.time_stamp_range), Date) == tsr_date,
            TrainerAvailability.availability_type == AvailabilityType.ADHOC
        ).exists()

        tsr_start = getTime(tsr.lower)
        tsr_end = getTime(tsr.upper)
        hasOpenRecurring = session.query(TrainerAvailability).filter(
            TrainerAvailability.trainer_email == Trainer.email,
            TrainerAvailability.availability_type == AvailabilityType.RECURRING,
            func.extract('dow', func.lower(TrainerAvailability.time_stamp_range)) == func.extract('dow', func.lower(tsr)),
            cast(func.lower(TrainerAvailability.time_stamp_range), Time) <= tsr_start,
            cast(func.upper(TrainerAvailability.time_stamp_range), Time) >= tsr_end
        ).exists()

        hasGFC = session.query(GroupFitnessClass.id).filter(
            GroupFitnessClass.trainer_email == Trainer.email,
            GroupFitnessClass.time_stamp_range.op('&&')(tsr)
        ).exists()

        hasPTS = session.query(PersonalTrainingSession.id).filter(
            PersonalTrainingSession.trainer_email == Trainer.email,
            PersonalTrainingSession.time_stamp_range.op('&&')(tsr)
        ).exists()

        conditions = and_(and_(or_(hasOpenAdhoc, and_(not_(hasOtherAdhocOnDate), hasOpenRecurring)), not_(hasGFC)), not_(hasPTS))

        trainers = session.query(Trainer.email).filter(conditions).distinct().all()
        
        result = []
        for trainer in trainers:
            result.append(trainer.email)
        
        return result

# tsr: DateTimeRange *Must be on the same day*
# Returns a list of room ids (Int)
def getAvailableRooms(engine, tsr):
    with Session(engine) as session:
        hasGFC = session.query(GroupFitnessClass.id).filter(
            GroupFitnessClass.room_id == Room.room_id,
            GroupFitnessClass.time_stamp_range.op('&&')(tsr)
        ).exists()

        hasPTS = session.query(PersonalTrainingSession.id).filter(
            PersonalTrainingSession.room_id == Room.room_id,
            PersonalTrainingSession.time_stamp_range.op('&&')(tsr)
        ).exists()

        conditions = and_(not_(hasGFC), not_(hasPTS))

        rooms = session.query(Room.room_id).filter(conditions).distinct().all()

        result = []
        for room in rooms:
            result.append(room.room_id)
        
        return result

def getDOW(ts):
    return ts.strftime('%A')

def getDate(ts):
    return ts.strftime('%Y-%m-%d')

def getTime(ts):
    return ts.strftime('%H:%M')