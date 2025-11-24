from sqlalchemy import text

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