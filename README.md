# **COMP 3005 Final Project**

## **COMP 3005 - Database Management Systems (Fall 2025)**

### **Group Members**
* Neil Varshney (101295007)
* Michael Fong (101300972)
* Liam McAnulty (101309972)

### Project Video Demo Link
Video Link: https://www.youtube.com/watch?v=k8grCX1jnFY 
* Subtitles are available for the video

### **Project Overview**
This project implements a Health and Fitness Club management system using PostgreSQL, Python, and SQLAlchemy (ORM). This program supports three roles which are Members, Trainers, and Administrators. The program handles core operations including member profiles, health metrics, billings, group fitness classes, maintenance, etc.

The database schema consists of 15 3NF normalized tables with foreign keys, constraints, and relationships. The system also includes a database for querying unpaid bills, a trigger that sets payment dates when the bill is paid, and an index on the ParticipatesIn table on the class_id column. This system uses SQLAlchemy ORM for most of the database operations with bidirectional relationships. Limited use of raw SQL is present due to querying database views  and creating triggers since direct ORM mapping is impractical for this functionality. 

The system provides a foundation for managing a fitness club’s daily operations with the use of proper database design.

### **Tech Stack**
* Language: Python
* Database: PostgreSQL
* ORM: SQLAlchemy
* Interface: CLI

### **Setup & How to Run**
1. Prerequisites
    These are the requirements needed to run this project on your computer:
    * Python 3.10+
    * PostgreSQL (Make sure the service is running)
    * psycopg2 library

2. Clone the Repository
    1. Open your terminal or command prompt and run the following commands to download the project:
        ```git clone https://github.com/mfong9164/COMP-3005--Final-Project```
    2. Navigate into the project directory:
        ```cd COMP-3005--Final-Project```
    3. In the root directory, install the required library of psycopg2 by writing the following in the terminal:
     ```pip install sqlalchemy psycopg2```
     
3. Database Configuration
    1. Open pgAdmin or your terminal and create a new database called "Health and Fitness Club Management System"
    2. in COMP-3005--Final-Project\app\main.py, ensure Database Configuration variables are set to your database credentials (lines 37-40)

4. Running the Program
    1. From the root project directory, navigate to the /app directory by typing the following in the terminal: ```cd app```
    2. Run the main application file: ```python main.py```
    3. Follow the CLI Interface. The program inserts sample data once it starts, and drops all data once it ends.


### **Implemented Functionalities**
**We implemented the following functionality:**
* Member Functions:
    * User Registration: Create a new member with unique email and basic profile info.
    * Profile Management: Update personal details, fitness goals (e.g., weight target), and input new health metrics (e.g., weight, heart rate).
    * Health History: Log multiple metric entries; do not overwrite. Must support time-stamped entries.
    * Dashboard: Show latest health stats, active goals, past class count, upcoming sessions.
    * Group Class Registration: Register for scheduled classes if capacity permits.

* Trainer Functions:
    * Set Availability: Define time windows when available for sessions or classes. Prevent overlap.
    * Schedule View: See assigned PT sessions and classes.
    * Member Lookup: Search by name (case-insensitive) and view current goal and last metric. No editing rights.

* Admin Functions:
    * Room Booking: Assign rooms for sessions or classes. Prevent double-booking.
    * Equipment Maintenance: Log issues, track repair status, associate with room/equipment.
    * Class Management: Define new classes, assign trainers/rooms/time, update schedules.
    * Billing & Payment: Generate bills, add line items, record payments. Simulate status updates.

* Trigger, View, & Index:
    * The **view** we created was a view that would display all unpaid bills with the admin, member, and bill information for that bill. It is called "unpaid_bills_view". We created this view because we thought that as we get more members within this application, the number of bills and unpaid bills would increase, meaning querying for them would be very often. Creating this view would make it more efficient by pre-joining the necessary tables and pre-filtering the records on bills that status is unpaid. This would reduce query complexity, as well as improve the performance of the admin dashboard.
    * One of the **triggers** we created was a trigger that would  automatically set the paid_date to the current date once a bill is paid. It is called "trigger_set_paid_date". This trigger works by being called once a bill has been paid and checks if the old value of bill.paid changed from False to True, which means the bill has been paid and sets the current date to the paid_date. This would allow for users to accurately see when a bill has been paid.
    * The **index** we created was on the class_id in the ParticipatesIn model in our system. To do this, we simply included a parameter index=True when creating the column for the model. This would make it so when querying for records in this table, it will be more efficient, especially if the table has large amounts of records. In this system, as the amount of users gets large, the number of members and classes would become large as it also stores previous classes and not just future classes. This means, when checking for bills, or class capacity, or something else that requires checking who or how many participants there are for a class, it will be more efficient on the DBMS if using an index.

### ORM Integration (SQLAlchemy)
We chose SQL Alchemy to map our PostgreSQL schema to our Python classes. This allowed us to use maintainable, object-oriented code instead of raw SQL. SQLAlchemy handles relationships, foreign keys, and constraints. It also supports automatic session management and type safety which improves code quality and maintainability. This allowed us to work with Python objects and relationships (ex, ```member.bills```, ```bill.group_fitness_bills```) rather than manual joins and SQL strings.

For example, the member entity shows ORM mapping, relationships, and lazy loading. The columns are created with types and constraints, and uses ```relationship()``` with ```back_populates``` to create a bidirectional one-to-many link. These relationships are lazy loaded, which means the data is loaded on access with a separate query. For example, ```bills = relationship("Bill", back_populates = "member", lazy='select')``` creates a link where ```member.bills``` returns all bills for that member, and ```bills.member``` returns all bills associated with that member. This logic is used across our entities which allows us to access object attributes with manual SQL joins. However, across our application, there may be times where we want to bundle several joins to get related data across several entities which would be inefficient if doing this in separate queries. So we use eager loading to bundle the query into 1 database trip to get all the data needed for that specific entity. Examples of ORM usage can be seen below.

**ORM Query Example:**
```python
# From member_func.py
member = session.query(Member).filter_by(email=member_email).first()
```

**ORM Insertion Example:**
```python
# From member_func.py
new_metric = HealthMetric(
    member_email=member_email,
    height=height,
    weight=weight,
    heart_rate=heart_rate
)
session.add(new_metric)
session.commit()
```

**ORM Update Example:**
```python
# From member_func.py
member.name = new_name
member.phone_number = new_phone
session.commit()
```

**ORM Relationship Access:**
```python
# From member_func.py - accessing bills through relationship which is lazy loaded (seperate queries)
bills = member.bills
for bill in bills:
    print(bill.amount_due)
```
**ORM Eager Loaded Query**
```python
# using selectinload to load all bills with their related data upfront
# selectinload uses separate SELECT queries with IN clause, which is efficient for multiple relationships
# this loads member, group_fitness_bills, and fitness_class all at once
# without eager loading, each bill.member and bill.group_fitness_bills access would trigger new queries
bills = session.query(Bill).options(selectinload(Bill.member), selectinload(Bill.group_fitness_bills).joinedload(GroupFitnessBill.fitness_class)).order_by(Bill.id.desc()).all()
```

**ORM Many-to-Many Access:**
```python
# From admin_func.py - accessing related entities
if bill.group_fitness_bills:  # Uses relationship
    for gf_bill in bill.group_fitness_bills:
        class_obj = gf_bill.fitness_class  # Another relationship access
```

### ER Model, Relational Schema Mapping, Normalization
* We created the **ER Model** based on the project requirement and the roles of each type of user and the functionality we were going to implement. View the ERD.pdf file to see ER Model: [ERD.pdf](/docs/ERD.pdf)
* We **mapped our ER Model into relational tables** by using the methods learned based on cardinality between relationships and foreign keys. View the ERD.pdf file to see ER Model Mapping to Relational Schema: [ERD.pdf](/docs/ERD.pdf)
* The database schema was already **normalized to 3NF Normalization**. This means each table’s attributes have no repeating groups or multi-valued attributes, All non-key attributes fully depend on the primary key of that table, and no transitive dependencies (all attributes depend directly on the primary key). We ensured that when creating the entites and schema we would avoid normalization issues in the future. View the ERD.pdf file to see Normalization Analysis: [ERD.pdf](/docs/ERD.pdf)

