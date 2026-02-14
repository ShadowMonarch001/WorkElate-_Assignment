# WorkElate AI Internship — Stateful Execution Agent

## Overview

This repository contains my submission for the WorkElate AI Internship **Stateful Execution Agent** task. The goal was to build a system capable of **planning → execution → memory → continuation**, demonstrating AI as an operational layer, not just an API wrapper.

The project includes:

- A **SaaS Launch Plan Agent** that generates company launch plans.
- **Persistent memory** using FAISS for plan retrieval and question answering.
- A **menu interface** for generating new plans or QA on existing plans.

---

## What I Built

- **Plan Generation:** Generates structured launch plans for any SaaS product based on a product brief.  
- **Memory System:** Stores plan sections in FAISS with embeddings to allow contextual retrieval.  
- **QA Mode:** Lets users ask questions about the generated plan; retrieves relevant sections from memory.  
- **Persistence:** Plans are saved to JSON, and memory can be reconstructed from saved files.  

---

## Thought Process

### 1. What Confused Me

- Managing **state across multiple sessions** was tricky.  
- Deciding **when to load memory vs. generate new plans** required careful handling to avoid overwriting existing data.  
- Structuring prompts for the LLM to **output strict JSON** while staying tactical and numerical needed multiple iterations.  

### 2. What I Would Change About the Task

- Isolate **data per company/product**. For example, Company A vs. Company B, so memory retrieval doesn’t mix contexts which i couldnt implement
- Add a **simple CLI dashboard** to visualize plan sections and key KPIs instead of relying solely on QA.  
- Include **automatic plan versioning**, so updates don’t overwrite previous versions.  

### 3. What Blocker Ate Most Time

- **Memory management:** setting up FAISS embeddings, ensuring correct retrieval, and reconstructing memory from JSON was the most time-consuming part.  
- **Prompt engineering:** handling invalid or partial JSON responses from the LLM needed careful exception handling.  

---

## How to Run
Set up your OpenRouter API key

Create a .env file in the project root:
Add your OpenRouter API key to the .env file:

```
OPENROUTER_API_KEY=your_api_key_here
```

```bash
# Clone the repo
git clone https://github.com/yourusername/stateful-execution-agent.git
cd stateful-execution-agent

# Install dependencies
pip install -r requirements.txt

# Run the main agent
python main.py
```

## Usage
# Product Brief

To generate a plan, make sure to update the product brief in `main.py`:

```python
brief = {
    "product_name": "BoardFlow",
    "target_users": "Remote product teams",
    "core_features": ["Task automation", "AI summaries", "Workflow tracking"],
    "timeline": "6 weeks",
    "budget": "$50,000"
}
```
- **Choose 1** to generate a new launch plan.  
- **Choose 2** to ask questions about an existing plan.  

Plans are saved to `launch_plan.json`.  

---

## Key Learnings

- Persistent, **stateful AI systems** are crucial for multi-step reasoning tasks.  
- Structuring prompts and **memory retrieval carefully** ensures accurate and actionable outputs.  
- **Isolating memory per use case** (e.g., per company/product) avoids cross-contamination of context.
- There are many more thing i need to add 
