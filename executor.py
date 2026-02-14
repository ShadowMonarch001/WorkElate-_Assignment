import json

def generate_section(section, state, memory, llm):
    # Retrieve relevant previous sections (top 2 for context)
    previous_sections = memory.retrieve_relevant(section, k=2)
    previous_text = "\n".join(
        [f"{s['section']}: {s['content']}" for s in previous_sections]
    )

    prompt = f"""
You are a SaaS strategy agent.
Generate a highly specific, tactical, and realistic output.

Avoid generic statements.
Avoid obvious advice.
Use numbers, assumptions, and concrete actions based on the information provided.
Think like a Series A SaaS founder preparing for execution.

Be opinionated and decisive.

Return STRICT JSON.
No markdown.
No headings.
No explanations.
No reasoning.

Section: {section}

Product Brief:
{state.brief}

Previous Context:
{previous_text}

Return output in this format:
{{
  "section": "{section}",
  "content": {{
      "key_points": [],
      "details": []
  }}
}}
"""

    raw_result = llm(prompt)

    try:
        parsed = json.loads(raw_result)
        return parsed
    except json.JSONDecodeError:
        return {
            "section": section,
            "content": {"error": "Invalid JSON returned"}
        }
