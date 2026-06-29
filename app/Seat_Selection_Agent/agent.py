import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

API_BASE = "http://127.0.0.1:5000/api"

def get_booking_info(pnr: str) -> dict:
    """Retrieve passenger details and seat info for a booking PNR."""
    try:
        res = requests.get(f"{API_BASE}/booking/{pnr}")
        return {"success": True, "data": res.json()} if res.status_code == 200 else {"success": False, "message": "PNR not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_seat_layout(flight_number: str) -> dict:
    """Fetch seat map for a flight showing available and booked seats."""
    try:
        res = requests.get(f"{API_BASE}/aircraft/{flight_number}/layout")
        return {"success": True, "seats": res.json().get("seats", [])} if res.status_code == 200 else {"success": False, "message": "Layout not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def update_passenger_seat(pnr: str, passenger_id: str, seat_number: str, flight_number: str, confirmed: bool = False) -> dict:
    """Assign a seat to a passenger. For extra legroom seats confirmed must be True."""
    try:
        layout = get_seat_layout(flight_number)
        if not layout["success"]:
            return {"success": False, "message": "Unable to fetch seat layout"}
        seat = next((s for s in layout["seats"] if s["seat_number"] == seat_number), None)
        if not seat:
            return {"success": False, "message": f"Seat {seat_number} not found"}
        if seat.get("extra_legroom") == 1 and not confirmed:
            return {"success": False, "requires_confirmation": True, "message": f"Seat {seat_number} has extra legroom and costs $25 extra. Do you confirm?"}
        res = requests.put(f"{API_BASE}/booking/{pnr}/seat", json={"passenger_id": passenger_id, "seat_number": seat_number, "flight_number": flight_number})
        return {"success": res.status_code == 200, "message": res.json().get("message", res.text)}
    except Exception as e:
        return {"success": False, "message": str(e)}

llm = LiteLlm(model="openai/gpt-4o-mini", temperature=0.5)

root_agent = Agent(
    name="Seat_Selection_Agent",
    model=llm,
    instruction="You are a Seat Specialist. Extract PNR from conversation. Call get_booking_info to get passenger details. Call get_seat_layout to show available seats. For extra legroom seats inform about $25 fee and wait for confirmation before calling update_passenger_seat with confirmed=True. Only handle seat and booking requests.",
    tools=[get_booking_info, get_seat_layout, update_passenger_seat]
)