from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from Travel_Agent.agent import root_agent as travel_agent
from Meal_Preference_Agent.agent import root_agent as meal_agent
from Seat_Selection_Agent.agent import root_agent as seat_agent

llm = LiteLlm(model="openai/gpt-4o-mini", temperature=0.5)

root_agent = Agent(
    name="Supervisor_Agent",
    model=llm,
    sub_agents=[meal_agent, seat_agent, travel_agent],
    instruction="Route meal/food/diet questions to Meal_Preference_Agent. Route seat/window/aisle/booking/PNR/passenger questions to Seat_Selection_Agent. Route visa/passport/entry/travel document questions to Travel_Agent. Never answer directly. Never explain."
)