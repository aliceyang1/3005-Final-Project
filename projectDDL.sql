-- DDL statements for Health and Fitness Club Management System

-- Members table
CREATE TABLE Members (
    Member_ID SERIAL PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    FullName VARCHAR(255) NOT NULL,
    Address TEXT,
    DateOfBirth DATE NOT NULL
);

-- Trainers table
CREATE TABLE Trainers (
    Trainer_ID SERIAL PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    Area VARCHAR(255)
);

-- Admins table
CREATE TABLE Admins (
    Admin_ID SERIAL PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    FullName VARCHAR(255) NOT NULL,
    Phone VARCHAR(20)
);

-- ExerciseRoutines table
CREATE TABLE ExerciseRoutines (
    Routine_ID SERIAL PRIMARY KEY,
    RoutineName VARCHAR(255) NOT NULL,
    Description TEXT,
    DifficultyLevel VARCHAR(50)
);

-- Rooms table
CREATE TABLE Rooms (
    Room_ID SERIAL PRIMARY KEY,
    RoomName VARCHAR(255) NOT NULL,
    Capacity INT NOT NULL
);

-- Equipment table
CREATE TABLE Equipment (
    Equipment_ID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(255) NOT NULL,
    Status VARCHAR(50),
    LastMaintenanceDate DATE
);

-- Sessions table
CREATE TABLE Sessions (
    Session_ID SERIAL PRIMARY KEY,
    DateTime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    Status VARCHAR(50),
    Member_ID INT REFERENCES Members(Member_ID),
    Trainer_ID INT REFERENCES Trainers(Trainer_ID),
    Room_ID INT REFERENCES Rooms(Room_ID)
);

-- Classes table
CREATE TABLE Classes (
    Class_ID SERIAL PRIMARY KEY,
    ClassName VARCHAR(255) NOT NULL,
    DateTime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    MaxParticipants INT,
    Room_ID INT REFERENCES Rooms(Room_ID),
    Trainer_ID INT REFERENCES Trainers(Trainer_ID)
);

-- Payments table
CREATE TABLE Payments (
    Payment_ID SERIAL PRIMARY KEY,
    PaymentDate DATE NOT NULL,
    PaymentMethod VARCHAR(50),
    Amount DECIMAL(10, 2) NOT NULL,
    Description TEXT,
    Member_ID INT REFERENCES Members(Member_ID),
    Admin_ID INT REFERENCES Admins(Admin_ID)
);

-- FitnessGoals (Goals) table
CREATE TABLE Goals (
    Goal_ID SERIAL PRIMARY KEY,
    Description TEXT,
    Status VARCHAR(50),
    Deadline DATE,
    Member_ID INT REFERENCES Members(Member_ID)
);

-- HealthMetrics table
CREATE TABLE HealthMetrics (
    Metric_ID SERIAL PRIMARY KEY,
    MetricType VARCHAR(255) NOT NULL,
    Value DECIMAL(10, 2) NOT NULL,
    Member_ID INT REFERENCES Members(Member_ID)
);

-- Availabilities table
CREATE TABLE Availabilities (
    Availability_ID SERIAL PRIMARY KEY,
    DateTime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    EntityType VARCHAR(255),
    Entity_ID INT
);

-- Associative table for Member and Class many-to-many relationship
CREATE TABLE Members_Classes (
    Member_ID INT REFERENCES Members(Member_ID),
    Class_ID INT REFERENCES Classes(Class_ID),
    PRIMARY KEY (Member_ID, Class_ID)
);

-- Associative table for Member and ExerciseRoutine many-to-many relationship
CREATE TABLE Members_Routines (
    Member_ID INT REFERENCES Members(Member_ID),
    Routine_ID INT REFERENCES ExerciseRoutines(Routine_ID),
    PRIMARY KEY (Member_ID, Routine_ID)
);

-- Associative table for Room and Availability many-to-many relationship
CREATE TABLE Rooms_Availabilities (
    Room_ID INT REFERENCES Rooms(Room_ID),
    Availability_ID INT REFERENCES Availabilities(Availability_ID),
    PRIMARY KEY (Room_ID, Availability_ID)
);

-- Associative table for Trainer and Availability many-to-many relationship
CREATE TABLE Trainers_Availabilities (
    Trainer_ID INT REFERENCES Trainers(Trainer_ID),
    Availability_ID INT REFERENCES Availabilities(Availability_ID),
    PRIMARY KEY (Trainer_ID, Availability_ID)
);
