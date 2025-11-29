# COMP-3005--Final-Project

## COMP 3005 - Database Management Systems (Fall 2025)

### Group Members
* Neil Varshney (101295007)
*
* 

### Project Video Demo Link

### Project Overview
This project implements a Health and Fitness Club management system using PostgreSQL, Python, and SQLAlchemy (ORM). This program supports three roles which are Members, Trainers, and Administrators. The program handles core operations including member profiles, health metrics, billings, group fitness classes, maintenance, etc.

The database schema consists of 15 3NF normalized tables with foreign keys, constraints, and relationships. The system also includes a database for querying unpaid bills, a trigger that sets payment dates when the bill is paid, and an index on the ParticipatesIn table on the class_id column. This system uses SQLAlchemy ORM for most of the database operations with bidirectional relationships. Limited use of raw SQL is present due to querying database views  and creating triggers since direct ORM mapping is impractical for this functionality. 

The system provides a foundation for managing a fitness club’s daily operations with the use of proper database design.

### Setup & How to Run
1. Prerequisites
    Ensure you have the following downloaded and intalled on your computer:
    * Python 3.10+
    * PostgreSQL (Make sure the service is running)

2. Database Configuration
    1. Open pgAdmin or your terminal and create a new database called "Health and Fitness Club Management System"
    2. 

### Implemented Functionalities 

