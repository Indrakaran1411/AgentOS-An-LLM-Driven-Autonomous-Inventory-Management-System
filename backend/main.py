from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import psycopg2
import json
import os

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB", "agent_os"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password")
    )

class UserQuery(BaseModel):
    text: str

def update_inventory(sku: str, change: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Ensure SKU is uppercase to match your init.sql
        cur.execute(
            "UPDATE inventory SET quantity = quantity + %s WHERE sku = %s",
            (change, sku.upper().strip())
        )
        conn.commit()
        count = cur.rowcount
        cur.close()
        conn.close()
        return count > 0
    except Exception as e:
        print(f"DB Error: {e}")
        return False

@app.post("/api/chat")
async def chat_with_agent(query: UserQuery):
    system_instructions = (
        "You are an inventory assistant. "
        "Return ONLY JSON. "
        "If selling: {\"action\": \"UPDATE\", \"sku\": \"SKU\", \"change\": -1} "
        "If returning: {\"action\": \"UPDATE\", \"sku\": \"SKU\", \"change\": 1}"
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": query.text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )
        
        ai_response = chat_completion.choices[0].message.content
        print(f"AI Response: {ai_response}")

        if "UPDATE" in ai_response:
            # Extract JSON
            start = ai_response.find('{')
            end = ai_response.rfind('}') + 1
            data = json.loads(ai_response[start:end])
            
            sku = data.get("sku")
            change = data.get("change")
            
            if update_inventory(sku, change):
                verb = "decreased" if change < 0 else "increased"
                return {"status": "success", "message": f"✅ Inventory {verb} for {sku}"}
            else:
                return {"status": "error", "message": f"❌ SKU {sku} not found."}

        return {"status": "chat", "message": ai_response}

    except Exception as e:
        # This will show the actual error in your terminal!
        print(f"DEBUG ERROR: {e}")
        return {"status": "error", "message": f"System Error: {str(e)}"}