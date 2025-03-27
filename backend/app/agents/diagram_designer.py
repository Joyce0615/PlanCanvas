from typing import Any, Dict

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage

from .base import AgentOutput, BaseAgent


class DiagramDesignerAgent(BaseAgent):
    """Agent responsible for creating and modifying Excalidraw diagrams."""
    
    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model=model)
        
        # System prompt for the diagram designer
        self.system_prompt = SystemMessage(content="""You are a diagram designer agent that creates and modifies Excalidraw diagrams.
Your role is to:
1. Convert design requirements into visual diagrams
2. Structure components in a clear and logical layout
3. Use appropriate shapes and connectors to show relationships
4. Maintain consistent styling and visual hierarchy

Focus on clarity and simplicity in your diagrams. Use standard shapes and clear labels.
Output diagram specifications in a structured JSON format compatible with Excalidraw.""")
    
    @property
    def name(self) -> str:
        return "DiagramDesigner"
    
    @property
    def description(self) -> str:
        return "Creates and modifies architecture diagrams using Excalidraw"
    
    async def process_message(self, message: str, context: Dict[str, Any]) -> AgentOutput:
        """Process a diagram-related request.
        
        Args:
            message: The diagram request/instructions
            context: Current context including existing diagram state
            
        Returns:
            AgentOutput with diagram changes and metadata
        """
        current_diagram = context.get("diagram", {})
        
        prompt = ChatPromptTemplate.from_messages([
            self.system_prompt,
            ("user", f"""Current diagram state:
{current_diagram}

Request: {message}

Generate an Excalidraw-compatible diagram specification that:
1. Addresses the request
2. Maintains any existing components
3. Uses clear shapes and labels

Output the diagram specification in this format:
DIAGRAM_SPEC: {{
  "elements": [
    {{
      "type": "rectangle|ellipse|diamond|arrow",
      "x": number,
      "y": number,
      "width": number,
      "height": number,
      "label": "string",
      "id": "string"
    }},
    ...
  ]
}}""")
        ])
        
        # Get the diagram specification from the LLM
        response = await self.llm.ainvoke(prompt)
        
        # Extract the JSON spec from the response
        content = response.content
        spec_start = content.find("DIAGRAM_SPEC:")
        if spec_start != -1:
            diagram_spec = content[spec_start + len("DIAGRAM_SPEC:"):].strip()
        else:
            diagram_spec = content
        
        return AgentOutput(
            content=content,
            metadata={"diagram_spec": diagram_spec}
        )
    
    async def can_handle_task(self, task: str) -> bool:
        """Check if this agent can handle the diagram-related task."""
        diagram_keywords = [
            "diagram", "draw", "visual", "layout", "component",
            "connection", "arrow", "box", "shape", "excalidraw"
        ]
        return any(keyword in task.lower() for keyword in diagram_keywords) 