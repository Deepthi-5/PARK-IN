-- DROP DATABASE PARKIN;
CREATE DATABASE IF NOT EXISTS PARKIN;
USE PARKIN;

CREATE TABLE IF NOT EXISTS User(
    U_id INTEGER AUTO_INCREMENT,
    Username VARCHAR(20) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Password VARCHAR(10) NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    V_no VARCHAR(12) NOT NULL,
    V_type VARCHAR(20),
    PRIMARY KEY(U_id)
);

CREATE TABLE IF NOT EXISTS Operator(
    O_id INTEGER AUTO_INCREMENT,
    Operatorname VARCHAR(20) UNIQUE NOT NULL,
    Password VARCHAR(20) NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    location VARCHAR(20) NOT NULL,
    floors INTEGER NOT NULL,
    slot_per_floor INTEGER NOT NULL,
    Rate_per_hour DECIMAL(10,2) NOT NULL,
    -- upper BIT(1) NOT NULL,
    PRIMARY KEY(O_id)
);

CREATE TABLE IF NOT EXISTS Slot_management(
    O_id INTEGER NOT NULL,
    Floor_no INTEGER NOT NULL,
    Slot_no VARCHAR(20) NOT NULL,
    -- upper BIT(1) NOT NULL,
    Occupancy BIT(1) NOT NULL,
    U_id INTEGER,
    PRIMARY KEY (O_id, Floor_no, Slot_no),
    FOREIGN KEY(O_id) REFERENCES Operator(O_id),
    FOREIGN KEY(U_id) REFERENCES User(U_id)
);

-- Booking and Payment related tables
CREATE TABLE IF NOT EXISTS Booking (
    Booking_id INTEGER AUTO_INCREMENT,
    U_id INTEGER NOT NULL,
    O_id INTEGER NOT NULL,
    Floor_no INTEGER NOT NULL,
    Slot_no VARCHAR(20) NOT NULL,
    Date DATE NOT NULL,
    InTime TIME NOT NULL,
    OutTime TIME NOT NULL,
    Price INTEGER,
    IsActive BIT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (Booking_id),
    FOREIGN KEY (U_id) REFERENCES User(U_id),
    FOREIGN KEY (O_id) REFERENCES Operator(O_id)
);

CREATE TABLE IF NOT EXISTS Payment (
    Payment_id INTEGER AUTO_INCREMENT,
    Booking_id INTEGER NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Payment_date DATE NOT NULL,
    PRIMARY KEY (Payment_id),
    FOREIGN KEY (Booking_id) REFERENCES Booking(Booking_id)
);

-- Feedback related tables
CREATE TABLE IF NOT EXISTS Feedback (
    Feedback_id INTEGER AUTO_INCREMENT,
    U_id INTEGER NOT NULL,
    O_id INTEGER NOT NULL,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Comment TEXT,
    PRIMARY KEY (Feedback_id),
    FOREIGN KEY (U_id) REFERENCES User(U_id),
    FOREIGN KEY (O_id) REFERENCES Operator(O_id)
);

-- Reminder System related tables (assuming reminders are related to bookings)
CREATE TABLE IF NOT EXISTS Reminder (
    Reminder_id INTEGER AUTO_INCREMENT,
    Booking_id INTEGER NOT NULL,
    Reminder_date DATE NOT NULL,
    PRIMARY KEY (Reminder_id),
    FOREIGN KEY (Booking_id) REFERENCES Booking(Booking_id)
);


-- SELECT * FROM Slot_management;
-- INSERT INTO Operator VALUES (1,"Forum_Mall","Bengaluru",3,10); 

SELECT U.Username, U.V_no as Vehicle_Number, U.Phone, F.Comment, F.Date, F.Time
FROM Feedback F INNER JOIN User U ON F.U_id = U.U_id WHERE F.O_id = 1 ORDER BY F.Date, F.Time ASC;

