from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .core.registry import AgentRegistry
from .agents.planner import PlannerAgent


class DesignRequest(BaseModel):
    prompt: str


class DesignResponse(BaseModel):
    plan: str
    diagram: dict
    log: list[str]


app = FastAPI(title="PlanCanvas API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent registry
registry = AgentRegistry()
registry.discover_agents()


@app.post("/api/design", response_model=DesignResponse)
async def create_design(request: DesignRequest) -> DesignResponse:
    """Create a new design based on the provided prompt."""
    try:
        # Initialize context
        context = {
            "diagram": {},
            "log": []
        }
        
        # Get the planner agent
        planner = PlannerAgent()
        
        # Process the initial request through the planner
        plan_output = await planner.process_message(request.prompt, context)
        context["log"].append(f"[{planner.name}] {plan_output.content}")
        
        # If the planner assigned a task to another agent, process it
        if plan_output.metadata and "assigned_to" in plan_output.metadata:
            assigned_agent_name = plan_output.metadata["assigned_to"]
            try:
                agent_cls = registry.get_agent(assigned_agent_name)
                agent = agent_cls()
                agent_output = await agent.process_message(
                    plan_output.metadata["context"],
                    context
                )
                context["log"].append(f"[{agent.name}] {agent_output.content}")
                
                # If this was the diagram designer, update the diagram
                if "diagram_spec" in agent_output.metadata:
                    context["diagram"] = agent_output.metadata["diagram_spec"]
            except KeyError:
                context["log"].append(f"Warning: Agent {assigned_agent_name} not found")
        
        return DesignResponse(
            plan=plan_output.content,
            diagram=context["diagram"],
            log=context["log"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agents": [agent.name for agent in registry.list_agents()]}
