
-- Insert sample Members
INSERT INTO Members (Username, Password, Email, FullName, Address, DateOfBirth)
VALUES
('jdoe', 'password123', 'jdoe@example.com', 'John Doe', '123 Maple Street', '1980-01-15'),
('asmith', 'password123', 'asmith@example.com', 'Alice Smith', '456 Oak Avenue', '1990-05-22'),
('bjones', 'password123', 'bjones@example.com', 'Bob Jones', '789 Pine Road', '1985-09-09');

-- Insert sample Trainers
INSERT INTO Trainers (FullName, Area)
VALUES
('Chris Johnson', 'Cardio'),
('Patricia Lee', 'Strength Training'),
('Kimberly Taylor', 'Yoga');

-- Insert sample Admins
INSERT INTO Admins (Email, FullName, Phone)
VALUES
('admin1@example.com', 'Admin One', '123-456-7890'),
('admin2@example.com', 'Admin Two', '234-567-8901');

-- Insert sample ExerciseRoutines
INSERT INTO ExerciseRoutines (RoutineName, Description, DifficultyLevel)
VALUES
('Beginner Yoga', 'A gentle introduction to yoga for beginners.', 'Beginner'),
('Cardio Blast', 'High-intensity cardio workouts to get your heart rate up.', 'Intermediate'),
('Strength Training Advanced', 'Advanced level strength training for experienced individuals.', 'Advanced');

-- Insert sample Equipment
INSERT INTO Equipment (EquipmentName, Status, LastMaintenanceDate)
VALUES
('Treadmill #1', 'Available', '2024-03-01'),
('Elliptical #8', 'Maintenance', '2024-03-15'),
('Dumbbell Set', 'Available', '2024-02-20');

-- Insert sample Sessions
INSERT INTO Sessions (DateTime, Status, Member_ID, Trainer_ID, Room_ID)
VALUES
('2024-04-15 08:00:00', 'Scheduled', 7, 7, 3),
('2024-04-16 09:00:00', 'Completed', 8, 8, 4);

-- Insert sample Classes
INSERT INTO Classes (ClassName, DateTime, MaxParticipants, Room_ID, Trainer_ID)
VALUES
('Morning Yoga', '2024-04-15 07:00:00', 20, 3, 7),
('Evening Cardio', '2024-04-16 18:00:00', 15, 4, 7);

-- Insert sample Rooms
INSERT INTO Rooms (RoomName, Capacity)
VALUES
('Yoga Studio', 20),
('Cardio Room', 15);

-- Insert sample Payments
INSERT INTO Payments (PaymentDate, PaymentMethod, Amount, Description, Member_ID, Admin_ID,)
VALUES
('2024-04-10', 'Credit Card', 59.99, 'Monthly Membership Fee', 7, 6),
('2024-04-12', 'Credit Card', 89.99, 'Monthly Premium Membership Fee', 8, 5);

-- Insert sample FitnessGoals
INSERT INTO Goals (Description, Status, Deadline, Member_ID)
VALUES
('Lose 10 pounds', 'Active', '2024-12-31', 7),
('Run a marathon', 'Active', '2024-10-15', 8);

-- Insert sample HealthMetrics
INSERT INTO HealthMetrics (MetricType, Value, Member_ID)
VALUES
('Weight', 185.5, 7),
('Blood Pressure', 120, 7);

-- Insert sample Availabilities
INSERT INTO Availabilities (DateTime, EntityType, Entity_ID)
VALUES
('2024-04-15 08:00:00', 'Room', 7),
('2024-04-15 09:00:00', 'Trainer', 7);

-- Insert sample Members_Classes (associative table)
INSERT INTO Members_Classes (Member_ID, Class_ID)
VALUES
(7, 1),
(8, 2);

-- Insert sample Members_Routines (associative table)
INSERT INTO Members_Routines (Member_ID, Routine_ID)
VALUES
(7, 7),
(8, 9);

-- Insert sample Rooms_Availabilities (associative table)
INSERT INTO Rooms_Availabilities (Room_ID, Availability_ID)
VALUES
(3, 1);

-- Insert sample Trainers_Availabilities (associative table)
INSERT INTO Trainers_Availabilities (Trainer_ID, Availability_ID)
VALUES
(7, 2);

ALTER TABLE Payments
ADD COLUMN Status VARCHAR(50) DEFAULT 'Outstanding';
