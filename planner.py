SECTIONS = [
    "Product Positioning",
    "MVP Scope",
    "Launch Strategy",
    "KPIs",
    "Risk Analysis",
    "Execution Roadmap"
]

def create_plan(state):
    if not state.plan:
        state.plan = SECTIONS
    return state.plan

def next_section(state):
    for section in state.plan:
        if section not in state.completed_sections:
            return section
    state.status = "completed"
    return None
