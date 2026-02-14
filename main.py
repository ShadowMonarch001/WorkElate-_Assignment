# main.py

from state import AgentState
from agent import run_agent
from memory_faiss import MemoryFAISS
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()  

# ----------------------------
# OpenRouter LLM setup
# ----------------------------


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def llm(prompt):
    if not OPENROUTER_API_KEY:
        raise Exception("OPENROUTER_API_KEY is not set!")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "arcee-ai/trinity-large-preview:free",
            "messages": [
                {"role": "system", "content": "You are a SaaS launch strategy agent."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }
    )

    print("Status:", response.status_code)

    result = response.json()
    print("Response JSON:", result)

    if "choices" not in result:
        raise Exception(f"OpenRouter error: {result}")

    return result["choices"][0]["message"]["content"]



# ----------------------------
# Product brief
# ----------------------------
brief = {
    "product_name": "BoardFlow",
    "target_users": "Remote product teams",
    "core_features": ["Task automation", "AI summaries", "Workflow tracking"],
    "timeline": "6 weeks",
    "budget": "$50,000"
}

# ----------------------------
# Initialize agent state and memory
# ----------------------------
memory = MemoryFAISS()
memory_loaded = False

while True:
    print("\nWhat would you like to do?")
    print("1. Generate new launch plan")
    print("2. Ask questions about existing plan")
    print("3. Exit")

    choice = input("Enter choice (1/2/3): ").strip()

    # ----------------------------
    # GENERATE PLAN
    # ----------------------------
    if choice == "1":
        state = AgentState(brief)
        final_output = run_agent(state, memory, llm)

        with open("launch_plan.json", "w") as f:
            json.dump(final_output, f, indent=4)
        memory_loaded = True
        memory.load_from_json("launch_plan.json")
        print("Plan generated and memory rebuilt.")

    # ----------------------------
    # QA MODE
    # ----------------------------
    elif choice == "2":
        if not memory_loaded:
            try:
                memory.load_from_json("launch_plan.json")
                memory_loaded = True
            except FileNotFoundError:
                print("No plan found. Please generate a plan first.")
                continue
            except json.JSONDecodeError:
                print("Plan file is corrupted. Please generate a new plan.")
                continue

        while True:
            question = input("\nAsk a question (or type back): ").strip()
            if question.lower() == "back":
                break
            answer = memory.answer_question(question, memory, llm)
            print("\nAnswer:\n", answer)



    # ----------------------------
    # EXIT
    # ----------------------------
    elif choice == "3":
        print("Goodbye.")
        break

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")



