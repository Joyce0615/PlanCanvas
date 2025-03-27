from typing import Any, Dict, List

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage

from .base import AgentOutput, BaseAgent
from ..core.registry import AgentRegistry


class PlannerAgent(BaseAgent):
    """Agent responsible for planning and orchestrating the design process."""
    
    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model=model)
        self.registry = AgentRegistry()
        
        # System prompt for the planner
        self.system_prompt = SystemMessage(content="""You are a planning agent responsible for breaking down design tasks and coordinating with other specialized agents.
Your role is to:
1. Break down complex design requests into smaller, manageable tasks
2. Identify which specialized agent should handle each task
3. Maintain the overall design context and ensure consistency
4. Integrate feedback and suggestions from other agents

Be strategic and methodical in your planning. Consider dependencies between tasks and aim for an efficient workflow.""")
    
    @property
    def name(self) -> str:
        return "Planner"
    
    @property
    def description(self) -> str:
        return "Coordinates the design process by breaking down tasks and delegating to specialized agents"
    
    async def process_message(self, message: str, context: Dict[str, Any]) -> AgentOutput:
        """Process an input message and plan the next steps.
        
        Args:
            message: The input message/request
            context: Current context including design state
            
        Returns:
            AgentOutput with planned next steps and any metadata
        """
        # Create a prompt that includes available agents and context
        available_agents = self.registry.list_agents()
        agent_descriptions = "\n".join([f"- {agent.name}: {agent.description}" 
                                      for agent in available_agents])
        
        prompt = ChatPromptTemplate.from_messages([
            self.system_prompt,
            ("user", f"""Available agents:
{agent_descriptions}

Current request: {message}

Current context:
{context}

Plan the next steps, considering:
1. What needs to be done next
2. Which agent should handle it
3. What information they need

Respond in a structured format:
NEXT_STEP: (describe the immediate next action)
ASSIGNED_TO: (name of the agent to handle it)
CONTEXT: (relevant context/instructions for the agent)""")
        ])
        
        # Get the plan from the LLM
        response = await self.llm.ainvoke(prompt)
        
        # Parse the response into structured data
        lines = response.content.split("\n")
        plan = {}
        current_key = None
        
        for line in lines:
            if line.startswith("NEXT_STEP:"):
                current_key = "next_step"
                plan[current_key] = line.replace("NEXT_STEP:", "").strip()
            elif line.startswith("ASSIGNED_TO:"):
                current_key = "assigned_to"
                plan[current_key] = line.replace("ASSIGNED_TO:", "").strip()
            elif line.startswith("CONTEXT:"):
                current_key = "context"
                plan[current_key] = line.replace("CONTEXT:", "").strip()
            elif current_key and line.strip():
                plan[current_key] = plan.get(current_key, "") + "\n" + line.strip()
        
        return AgentOutput(
            content=response.content,
            metadata=plan
        )
    
    async def can_handle_task(self, task: str) -> bool:
        """The planner can handle any high-level task that needs coordination."""
        return True
