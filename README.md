

# SmartAirline-Agent ✈️
> An intelligent airline customer service chatbot powered by **Google ADK**, **Multi-Agent Architecture**, and **RAG** — built entirely from scratch.

## 🧠 How It Works
```
User Message → Supervisor Agent → Seat Agent / Meal Agent / Travel Agent
                                        ↓              ↓            ↓
                                  FastAPI+SQLite  FastAPI+SQLite  ChromaDB RAG
```

## 🤖 Agents
| Agent | Responsibility |
|-------|---------------|
| Supervisor Agent | Intent detection and routing |
| Seat Selection Agent | Seat queries, layout, assignments with legroom gate |
| Meal Preference Agent | Meal updates validated against catalog |
| Travel Document Agent | RAG-powered visa and passport queries |

## 📚 RAG Pipeline
```
PDF → Chunking → Embeddings → ChromaDB → Similarity Search → GPT Answer
```
Zero hallucination — answers only from retrieved document chunks.

## 🔌 API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/booking/{pnr}` | GET | Get passengers |
| `/api/booking/{pnr}/seat` | PUT | Update seat |
| `/api/booking/{pnr}/meal` | PUT | Update meal |
| `/api/aircraft/{flight}/layout` | GET | Seat map |
| `/api/meal/catalog` | GET | Meal options |

## 💬 Sample Conversations
```
User: Change meal for John Doe to Vegan for PNR001
Bot:  Meal for John Doe on flight AI203 updated to Vegan.

User: I want seat 1A for PNR002
Bot:  Seat 1A has extra legroom — $25 fee. Confirm?
User: Yes
Bot:  John Doe assigned to seat 1A on flight AI203.

User: Do I need a visa for Spain?
Bot:  Yes, Schengen visa required. Documents needed: application form, passport photo, 6 months validity...



example
## 📸 Demo

![Screenshot 1](screenshots/Screenshot%202026-06-29%20210128.png)

![Screenshot 2](screenshots/Screenshot%202026-06-29%20210736.png)

![Screenshot 3](screenshots/Screenshot%202026-06-29%20212446.png)
```

## 🛠️ Tech Stack
| Technology | Role |
|------------|------|
| Google ADK | Agent framework and routing |
| GPT-4o-mini | LLM brain inside every agent |
| FastAPI + SQLite | Mock airline backend |
| ChromaDB | Vector database |
| Sentence Transformers | Text embeddings |
| LangChain | PDF loading and chunking |

## ▶️ Getting Started
```bash
pip install -r requirements.txt
python travel_kb_builder.py
python API_Server.py        # Terminal 1
adk web app                 # Terminal 2
```
Open `http://127.0.0.1:8000` and select Supervisor_Agent.

## 🔮 Future Enhancements
- Baggage Management Agent
- Flight Booking Agent
- Live Airline API Integration
- Multi-language Support
- Voice Interaction

## 📌 Objective
Demonstrates how **Generative AI**, **Multi-Agent Systems**, and **RAG** can build scalable, production-ready intelligent customer service solutions for the airline industry.

