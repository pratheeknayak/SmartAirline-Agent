--TABLE: Flight
CREATE TABLE IF NOT EXISTS flight (
    flight_number TEXT PRIMARY KEY,
    departure TEXT,
    destination TEXT,
    date TEXT,
    time TEXT,
    aircraft TEXT
);

-- TABLE: Seats
CREATE TABLE IF NOT EXISTS seats (
    seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT,
    seat_number TEXT,
    row_number INTEGER,
    column_letter TEXT,
    seat_class TEXT,
    seat_type TEXT,
    extra_legroom BOOLEAN,
    status TEXT,
    FOREIGN KEY (flight_number) REFERENCES flight(flight_number)
);

-- TABLE: Meal
CREATE TABLE IF NOT EXISTS meal (
    meal_name TEXT PRIMARY KEY
);

-- TABLE: Passengers
CREATE TABLE IF NOT EXISTS passengers (
    id TEXT PRIMARY KEY,      
    pnr TEXT,
    name TEXT NOT NULL,
    seat_id INTEGER,
    meal TEXT,
    loyaltytier TEXT,
    flight_number TEXT NOT NULL,
    FOREIGN KEY (seat_id) REFERENCES seats(seat_id),
    FOREIGN KEY (flight_number) REFERENCES flight(flight_number),
    FOREIGN KEY (meal) REFERENCES meal(meal_name)
);


------------------------------------------------
-- MOCK DATA
------------------------------------------------


-- Flights:
INSERT OR IGNORE INTO flight VALUES
('AI203','BLR','DEL','2026-04-10','10:30','A320'),
('AI204','DEL','BLR','2026-04-11','14:00','A320'),
('AI301','BLR','MUM','2026-04-12','09:00','B737'),
('AI302','MUM','BLR','2026-04-12','18:30','B737'),
('AI450','BLR','HYD','2026-04-13','07:45','A321');


-- Meals:
INSERT OR IGNORE INTO meal VALUES
('Veg'),
('Non-Veg'),
('Vegan'),
('Jain'),
('Gluten-Free'),
('Kosher');


-- Seats:
INSERT OR IGNORE INTO seats (flight_number,seat_number,row_number,column_letter,seat_class,seat_type,extra_legroom,status) VALUES
('AI203','1A',1,'A','Business','window',1,'available'),
('AI203','1B',1,'B','Business','aisle',1,'available'),
('AI203','2A',2,'A','Business','window',1,'booked'),
('AI203','10A',10,'A','Economy','window',0,'available'),
('AI203','10B',10,'B','Economy','middle',0,'booked'),
('AI203','10C',10,'C','Economy','aisle',0,'available'),
('AI203','11A',11,'A','Economy','window',0,'available'),
('AI203','11B',11,'B','Economy','middle',0,'available'),
('AI203','11C',11,'C','Economy','aisle',0,'available'),
('AI203','12A',12,'A','Economy','window',0,'blocked'),
('AI450','1B',1,'B','Business','aisle',1,'available'),
('AI450','20B',20,'B','Economy','aisle',0,'available'),
('AI302','2A',2,'A','Business','window',1,'booked'),
('AI302','10A',10,'A','Economy','window',0,'available'),
('AI302','11B',11,'B','Economy','middle',0,'available');

-- Passengers:
INSERT INTO passengers (id, pnr, name, seat_id, meal, loyaltytier, flight_number) VALUES
('PAX001', 'PNR001', 'John Doe', NULL, 'Veg', 'Gold', 'AI203'),
('PAX002', 'PNR001', 'Mary Doe', NULL, 'Non-Veg', 'Silver', 'AI203'),
('PAX003', 'PNR002', 'Rahul Sharma', 3, 'Vegan', 'Platinum', 'AI203'),
('PAX004', 'PNR003', 'Anita Singh', 5, 'Veg', 'Gold', 'AI203'),
('PAX005', 'PNR004', 'David Lee', NULL, 'Kosher', 'Silver', 'AI203'),
('PAX006', 'PNR005', 'Sara Khan', NULL, 'Jain', 'Gold', 'AI450'),
('PAX007', 'PNR006', 'Arjun Patel', NULL, 'Gluten-Free', 'Bronze', 'AI203'),
('PAX008', 'PNR006', 'Emily Clark', NULL, 'Veg', 'Silver', 'AI203'),
('PAX009', 'PNR005', 'Ajith Nair', NULL, 'Veg', 'Silver', 'AI450'),
('PAX0010', 'PNR005', 'Ajith Shetty', NULL, 'Veg', 'Gold', 'AI302');