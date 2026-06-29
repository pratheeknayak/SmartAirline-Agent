import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

API_BASE = "http://127.0.0.1:5000/api"

def get_booking_info(pnr: str) -> dict:
    """Retrieve passenger details and current meal for a booking PNR."""
    try:
        res = requests.get(f"{API_BASE}/booking/{pnr}")
        return {"success": True, "data": res.json()} if res.status_code == 200 else {"success": False, "message": "PNR not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_meal_catalog() -> dict:
    """Fetch all available meal options from the airline catalog."""
    try:
        res = requests.get(f"{API_BASE}/meal/catalog")
        return {"success": True, "meals": res.json().get("meals", [])} if res.status_code == 200 else {"success": False, "message": "Catalog unavailable"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def update_passenger_meal(pnr: str, passenger_id: str, meal_name: str) -> dict:
    """Update meal preference for a specific passenger in a booking."""
    try:
        res = requests.put(f"{API_BASE}/booking/{pnr}/meal", json={"passenger_id": passenger_id, "meal_name": meal_name})
        return {"success": True, "message": res.json().get("message")} if res.status_code == 200 else {"success": False, "message": res.json().get("detail", res.text)}
    except Exception as e:
        return {"success": False, "message": str(e)}

llm = LiteLlm(model="openai/gpt-4o-mini", temperature=0.5)

root_agent = Agent(
    name="Meal_Preference_Agent",
    model=llm,
    instruction="You are a Meal Specialist. Extract PNR from conversation. Call get_booking_info to get passengers. If multiple passengers ask which one. Call get_meal_catalog to show options if user has not specified. Call update_passenger_meal after valid selection. Confirm with passenger name flight and meal. Only use meals from catalog. Only handle meal requests.",
    tools=[get_booking_info, get_meal_catalog, update_passenger_meal]
)