from typing import Dict, Any
from ..agents.planner import PlannerAgent
from ..agents.diagram import DiagramDesignerAgent

class Orchestrator:
    """
    Coordinates the multi-agent process. For the MVP, we just chain:
      1) Planner -> 2) DiagramDesigner
    In later stages, we'll add more agent roles, iterative loops, logging, etc.
    """
    def __init__(self):
        self.planner_agent = PlannerAgent()
        self.diagram_agent = DiagramDesignerAgent()
        # You might store conversation logs or agent states here

    def run_design_session(self, prompt: str) -> Dict[str, Any]:
        # 1) The planner agent interprets the prompt and returns a plan
        plan, planner_log = self.planner_agent.create_plan(prompt)

        # 2) The diagram agent uses the plan to create a diagram representation
        diagram, diagram_log = self.diagram_agent.draw_diagram(plan)

        # For now, "diagram" might just be a stub (like a string "diagram placeholder").
        # In Phase 2, you'll generate real Excalidraw JSON or another structure.

        # Combine logs for demonstration:
        session_log = planner_log + "\n" + diagram_log

        return {
            "diagram": diagram,
            "log": session_log
        }
