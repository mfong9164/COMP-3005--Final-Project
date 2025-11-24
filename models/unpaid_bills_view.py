from sqlalchemy import text

def drop_unpaid_bills_view(engine):
    """Drop the unpaid_bills_view if it exists"""
    drop_view_sql = """
    DROP VIEW IF EXISTS unpaid_bills_view CASCADE;
    """
    
    with engine.connect() as conn:
        conn.execute(text(drop_view_sql))
        conn.commit()

def create_unpaid_bills_view(engine):
    ## create a view for unpaid bills with member and admin information. this will display bill information and the member
    ## associated with that if the bill is unpaid.
    
    view_sql = """
    CREATE OR REPLACE VIEW unpaid_bills_view AS
    SELECT 
        b.id AS bill_id,
        b.amount_due,
        b.payment_method,
        b.paid,
        m.email AS member_email,
        m.name AS member_name,
        m.phone_number AS member_phone,
        a.email AS admin_email,
        a.name AS admin_name
    FROM "Bill" b
    JOIN "Member" m ON b.member_email = m.email
    JOIN "Admin" a ON b.admin_email = a.email
    WHERE b.paid = FALSE;
    """
    
    with engine.connect() as conn:
        conn.execute(text(view_sql))
        conn.commit()
        print("View 'unpaid_bills_view' created successfully")