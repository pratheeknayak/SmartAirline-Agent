import uvicorn
import sqlite3
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
DB_DIR = os.path.join(BASE_DIR, "db_data")
DB_FILE = "airline_system.db"
DATABASE_PATH = os.path.join(DB_DIR, DB_FILE)

# SQL initialization script
INIT_SQL_SCRIPT = os.path.join(BASE_DIR, "Mock_DB.sql")

app = FastAPI(title="Airline Seat & Booking API")


class SeatUpdateRequest(BaseModel):
    passenger_id: str
    seat_number: str
    flight_number: str

class MealUpdateRequest(BaseModel):
    passenger_id: str
    meal_name: str


# DATABASE INITIALIZATION
def initialize_database():

    os.makedirs(DB_DIR, exist_ok=True)

    if not os.path.exists(DATABASE_PATH):
        connection = sqlite3.connect(DATABASE_PATH)

        with open(INIT_SQL_SCRIPT, "r") as file:
            sql_script = file.read()

        connection.executescript(sql_script)
        connection.commit()
        connection.close()

        print("Database created and initialized")
    else:
        print("Database already exists")


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
def startup_event():
    initialize_database()


# GET BOOKING DETAILS
@app.get("/api/booking/{pnr}")
def get_booking(pnr: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.name, p.pnr, p.meal, p.loyaltytier,
               p.flight_number, s.seat_number, f.departure, f.destination,
               f.date, f.time, f.aircraft
        FROM passengers p
        LEFT JOIN seats s ON p.seat_id = s.seat_id
        LEFT JOIN flight f ON p.flight_number = f.flight_number
        WHERE p.pnr = ?
    """, (pnr,))

    records = cursor.fetchall()
    conn.close()

    if not records:
        raise HTTPException(status_code=404, detail="PNR not found")

    passengers = []
    for row in records:
        passengers.append({
            "id": row['id'],    
            "name": row["name"],
            "seat": row["seat_number"] or "Not Assigned",
            "meal": row["meal"],
            "loyaltyTier": row["loyaltytier"],
            "flight": {
                "number": row["flight_number"],
                "departure": row["departure"],
                "destination": row["destination"],
                "date": row["date"],
                "time": row["time"],
                "aircraft": row["aircraft"]
            }
        })

    return {
        "pnr": pnr,
        "passengers": passengers
    }


# SEAT UPDATE:
@app.put("/api/booking/{pnr}/seat")
def update_seat(pnr: str, request: SeatUpdateRequest):

    conn = get_connection()
    cursor = conn.cursor()

    # Get new seat
    cursor.execute(
        "SELECT seat_id, status FROM seats WHERE seat_number=? AND flight_number=?",
        (request.seat_number, request.flight_number)
    )
    new_seat = cursor.fetchone()

    if not new_seat:
        conn.close()
        raise HTTPException(status_code=404, detail="Seat not found")

    if new_seat["status"] == "booked":
        conn.close()
        raise HTTPException(status_code=400, detail="Seat already booked")

    new_seat_id = new_seat["seat_id"]

    # Get current seat
    cursor.execute(
        "SELECT seat_id FROM passengers WHERE id=? AND flight_number=?",
        (request.passenger_id, request.flight_number)
    )
    current = cursor.fetchone()
    old_seat_id = current["seat_id"] if current else None

    # If same seat, do nothing
    if old_seat_id == new_seat_id:
        conn.close()
        return {"message": "Seat already assigned"}

    # Free old seat
    if old_seat_id:
        cursor.execute(
            "UPDATE seats SET status='available' WHERE seat_id=?",
            (old_seat_id,)
        )

    # Book new seat
    cursor.execute(
        "UPDATE seats SET status='booked' WHERE seat_id=?",
        (new_seat_id,)
    )

    # Update passenger
    cursor.execute(
        "UPDATE passengers SET seat_id=? WHERE id=?",
        (new_seat_id, request.passenger_id)
    )

    conn.commit()
    conn.close()

    return {"message": f"Seat {request.seat_number} assigned successfully"}

#Update meal
@app.put("/api/booking/{pnr}/meal")
def update_meal(pnr: str, request: MealUpdateRequest):

    conn = get_connection()
    cursor = conn.cursor()

    # Check passenger exists
    cursor.execute(
        "SELECT id FROM passengers WHERE id=? AND pnr=?",
        (request.passenger_id, pnr)
    )

    passenger = cursor.fetchone()

    if not passenger:
        conn.close()
        raise HTTPException(status_code=404, detail="Passenger not found")

    # Check meal exists in catalog
    cursor.execute(
        "SELECT meal_name FROM meal WHERE meal_name=?",
        (request.meal_name,)
    )

    meal = cursor.fetchone()

    if not meal:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid meal type")

    # Update meal
    cursor.execute(
        "UPDATE passengers SET meal=? WHERE id=? AND pnr=?",
        (request.meal_name, request.passenger_id, pnr)
    )

    conn.commit()
    conn.close()

    return {
        "message": f"Meal updated successfully to {request.meal_name}"
    }

# AIRCRAFT SEAT LAYOUT
@app.get("/api/aircraft/{flightId}/layout")
def get_aircraft_layout(flightId: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT seat_id, seat_number, row_number,
               column_letter, seat_class, seat_type,
               extra_legroom, status
        FROM seats
        WHERE flight_number=?
        ORDER BY row_number, column_letter
    """, (flightId,))

    seats = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {
        "flight_id": flightId,
        "seats": seats
    }


# MEAL CATALOG
@app.get("/api/meal/catalog")
def get_meals():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT meal_name FROM meal")

    meals = [row["meal_name"] for row in cursor.fetchall()]
    conn.close()

    return {"meals": meals}


# FLIGHT CONNECTIONS
@app.get("/api/flight/connections")
def get_flights():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT flight_number, departure,
               destination, date, time, aircraft
        FROM flight
    """)

    flights = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"flights": flights}


# RUN SERVER
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)