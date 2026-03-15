import json
import random

# Building blocks for our mock retail data
actions = [
    ("returned a damaged", "damaged_quarantine", "back_room", 1),
    ("purchased a", "sold", "front_store", -1),
    ("restocked a batch of", "available", "main_floor", 10),
    ("cannot find any", "stock_check", "null", 0)
]

items = [
    ("pair of black running shoes, size 10", "SHOE-BLK-RUN-10"),
    ("medium blue cotton shirt", "SHRT-BLU-COT-M"),
    ("wireless noise-canceling headphones", "TECH-HP-WNC-01"),
    ("pack of AAA batteries", "ELEC-BAT-AAA-12")
]

actors = ["A customer just", "The floor manager", "A warehouse associate"]

dataset = []

# Generate 200 mock interactions
for _ in range(200):
    action_text, status, location, qty = random.choice(actions)
    item_text, sku = random.choice(items)
    actor = random.choice(actors)
    
    # The natural language input
    user_prompt = f"{actor} {action_text} {item_text}."
    
    # The exact JSON we want the LLM to learn to output
    target_json = {
        "action": "inventory_adjustment" if qty != 0 else "inventory_query",
        "sku": sku,
        "quantity_change": qty,
        "status": status,
        "location": location
    }
    
    # Format for Mistral / OpenAI fine-tuning (JSONL format)
    training_example = {
        "messages": [
            {"role": "system", "content": "You are a Retail AgentOS. Convert operations queries into structured JSON actions."},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": json.dumps(target_json)}
        ]
    }
    dataset.append(training_example)

# Save to a JSONL file
with open("agentos_training_data.jsonl", "w") as f:
    for entry in dataset:
        f.write(json.dumps(entry) + "\n")

print(f"Successfully generated {len(dataset)} training examples in 'agentos_training_data.jsonl'")