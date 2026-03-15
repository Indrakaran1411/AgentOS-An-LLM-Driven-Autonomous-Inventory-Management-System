AgentOS: An LLM-Driven Autonomous Inventory Management System
AgentOS is a sophisticated, containerized AI agent designed to bridge the gap between natural language and relational database orchestration. Developed as a proof-of-concept for high-precision tracking environments (such as Aerospace component management), it leverages the reasoning capabilities of Large Language Models (LLMs) to manage complex inventory workflows autonomously.

🚀 The Vision
In high-stakes engineering environments, manual data entry is a bottleneck. AgentOS allows personnel to update stock levels using conversational text or voice-to-text, ensuring 100% database integrity through "Reasoning over SQL" logic.

✨ Core Features
Autonomous Intent Recognition: Utilizes Llama 3.3 (via Groq) to intelligently distinguish between sales (inventory reduction) and returns (inventory addition).

Entity Extraction: Automatically parses SKUs and quantities from raw, unstructured user input.

Transactional Integrity: Implements atomic SQL updates in PostgreSQL to prevent race conditions.

Containerized Architecture: Fully orchestrated using Docker Compose, ensuring "it runs on my machine" translates to "it runs everywhere."

🛠️ Tech Stack
Language: Python 3.9

AI Engine: Groq Cloud (Llama 3.3 70B Model)

Backend: FastAPI (Asynchronous REST API)

Frontend: Streamlit (Reactive Web UI)

Database: PostgreSQL 15

Orchestration: Docker & Docker Compose

📂 Project Structure
Plaintext
agent-os/
├── backend/
│   ├── main.py            # FastAPI Logic & Agent Reasoning
│   ├── Dockerfile         # Backend Containerization
│   └── requirements.txt   # Python Dependencies
├── frontend/
│   └── frontend.py        # Streamlit User Interface
├── db/
│   └── init.sql           # Relational Schema & Seed Data
├── .env                   # Environment Secrets (Ignored by Git)
└── docker-compose.yml     # Service Orchestration
🚦 Getting Started
1. Prerequisites
Docker & Docker Compose installed.

A Groq API Key (Available at console.groq.com).

2. Configuration
Create a .env file in the root directory:

Plaintext
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=agent_os
GROQ_API_KEY=your_groq_api_key_here
3. Deployment
Bash
# Start the entire stack
docker-compose up --build
4. Running the UI
In a separate terminal, launch the frontend:

Bash
cd frontend
pip install -r requirements.txt
streamlit run frontend.py
🧪 Live Demo Verification
Interaction: Enter "Sold 1x SHOE-BLK-RUN-10" in the Streamlit UI.

AI Reasoning: The system identifies the "Sale" intent and converts it to a -1 quantity change.

Database Sync: Verify the update directly in the container:

Bash
docker exec -it agentos_db psql -U user -d agent_os -c "SELECT * FROM inventory;"
Result: Quantity decreases from 50 to 49.

🎓 Academic Context
This project was developed by Indra Karan Gajula, a final-year Aerospace Engineering student at IIT Madras. It demonstrates the application of Generative AI in solving traditional engineering logistics and supply chain challenges.
