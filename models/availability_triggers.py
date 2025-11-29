from sqlalchemy import text

# Creates AFTER INSERT Trigger on Trainer table
# This will initialize the Trainer's schedule so that future changes can all be updates, rather than inserts
def create_init_trainer_availability_trigger(engine):
    function_sql = """
    CREATE OR REPLACE FUNCTION init_trainer_availability()
    RETURNS TRIGGER AS $$
    DECLARE
        i int;
        current timestamp := '1996-01-01 00:00:00';
        start_ts timestamp;
        end_ts timestamp;
    BEGIN
        FOR i IN 0..6 LOOP
            IF i <= 4 THEN
                start_ts := current + (9 || ' hours')::interval;
                end_ts := start_ts + (8 || ' hours')::interval;
            ELSE
                start_ts := current;
                end_ts := current + (1 || ' seconds')::interval;
            END IF;

            INSERT INTO "TrainerAvailability" (trainer_email, time_stamp_range, availability_type)
            VALUES (
                NEW.email,
                tsrange(start_ts, end_ts, '[)'),
                'RECURRING'
            );
            current := current + (1 || ' days')::interval;
        END LOOP;
        
        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    """

    trigger_sql = """
    DROP TRIGGER IF EXISTS trigger_init_trainer_availability on "Trainer";
    CREATE TRIGGER trigger_init_trainer_availability
    AFTER INSERT ON "Trainer"
    FOR EACH ROW
    EXECUTE FUNCTION init_trainer_availability();
    """

    with engine.connect() as conn:
        conn.execute(text(function_sql))
        conn.execute(text(trigger_sql))
        conn.commit()
        print("Trigger 'trigger_init_trainer_availability' created successfully")

# Checks If ...
# Time fits in Trainer's Availability Adhoc or Time fits in Trainer's Availability Recurring
# No exisiting group classes during class for Trainer or in Room
# No exisiting personal classes during class for Trainer or in Room
def check_class_time_trigger(engine):
    function_sql = """
    CREATE OR REPLACE FUNCTION check_class_time_trigger()
    RETURNS TRIGGER AS $$
    DECLARE
        adhocTA RECORD;
        recurringTA RECORD;
        groupClass RECORD;
        personalSession RECORD;
    BEGIN
        -- CHECK TRAINER'S AVAILABILITY --
        SELECT *
        INTO adhocTA
        FROM "TrainerAvailability" ta
        WHERE 
            ta.trainer_email=NEW.trainer_email AND
            ta.availability_type='ADHOC' AND
            NEW.time_stamp_range <@ ta.time_stamp_range;

        IF adhocTA IS NULL THEN        
            SELECT * 
            INTO recurringTA
            FROM "TrainerAvailability" ta
            WHERE
                ta.trainer_email=NEW.trainer_email AND
                ta.availability_type='RECURRING' AND
                extract(dow FROM lower(ta.time_stamp_range)) = extract(dow FROM lower(NEW.time_stamp_range)) AND
                lower(ta.time_stamp_range)::time <= lower(NEW.time_stamp_range)::time AND
                upper(ta.time_stamp_range)::time >= upper(NEW.time_stamp_range)::time;
            
            IF recurringTA IS NULL THEN
                RAISE EXCEPTION 'Trainer is not available during timeslot';
            END IF;
        END IF;

        -- CHECK TRAINER'S OTHER CLASSES AND ROOM AVAILABILITY --
        SELECT *
        INTO groupClass
        FROM "GroupFitnessClass" as fc
        WHERE
            (
                fc.trainer_email=NEW.trainer_email OR
                fc.room_id=NEW.room_id
            ) AND
            fc.time_stamp_range && NEW.time_stamp_range;
        
        IF groupClass IS NOT NULL 
        THEN
            RAISE EXCEPTION 'Trainer has a Group Fitness Class during this time';
        END IF;

        SELECT *
        INTO personalSession
        FROM "PersonalTrainingSession" as ts
        WHERE
            (
                ts.trainer_email=NEW.trainer_email OR
                ts.room_id=NEW.room_id
            ) AND
            ts.time_stamp_range && NEW.time_stamp_range;
        
        IF personalSession IS NOT NULL THEN
            RAISE EXCEPTION 'Trainer has a Personal Training Session during this time';
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

    trigger_sql = """
    DROP TRIGGER IF EXISTS check_class_time_trigger on "GroupFitnessClass";
    CREATE TRIGGER check_class_time_trigger
    BEFORE INSERT OR UPDATE ON "GroupFitnessClass"
    FOR EACH ROW
    EXECUTE FUNCTION check_class_time_trigger();

    DROP TRIGGER IF EXISTS check_class_time_trigger on "PersonalTrainingSession";
    CREATE TRIGGER check_class_time_trigger
    BEFORE INSERT OR UPDATE ON "PersonalTrainingSession"
    FOR EACH ROW
    EXECUTE FUNCTION check_class_time_trigger();
    """

    with engine.connect() as conn:
        conn.execute(text(function_sql))
        conn.execute(text(trigger_sql))
        conn.commit()
        print("Trigger 'check_class_time_trigger' created successfully")