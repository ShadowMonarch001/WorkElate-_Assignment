from planner import create_plan, next_section
from executor import generate_section
from reflection import reflect

def run_agent(state, memory, llm):
    create_plan(state)

    while state.status != "completed":
        section = next_section(state)
        if not section:
            break

        state.current_step = section

        output = generate_section(section, state, memory, llm)

        state.artifacts[section] = output
        state.completed_sections.append(section)

        # Store section in FAISS memory
        memory.store(section, output)

        reflect(output, state)

    return state.artifacts
