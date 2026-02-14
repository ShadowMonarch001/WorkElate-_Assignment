class AgentState:
    def __init__(self, brief):
        self.goal = "Launch SaaS Dashboard"
        self.brief = brief
        self.plan = []
        self.completed_sections = []
        self.artifacts = {}
        self.current_step = None
        self.reflections = []
        self.status = "running"
