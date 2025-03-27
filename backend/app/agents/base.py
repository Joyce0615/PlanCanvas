from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

from langchain.schema import BaseMessage
from pydantic import BaseModel


class AgentOutput(BaseModel):
    """Output from an agent's processing."""
    content: str
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """
    Base agent class. Agents should implement some consistent interface,
    for example, a method to handle input and produce output + log.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the agent."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what this agent does."""
        pass
    
    @abstractmethod
    async def process_message(self, message: str, context: Dict[str, Any]) -> AgentOutput:
        """Process a message and return a response.
        
        Args:
            message: The input message to process
            context: Shared context dictionary containing state like diagram data
            
        Returns:
            AgentOutput containing the response and any metadata
        """
        pass
    
    @abstractmethod
    async def can_handle_task(self, task: str) -> bool:
        """Determine if this agent can handle the given task.
        
        Args:
            task: Description of the task to be performed
            
        Returns:
            True if this agent can handle the task, False otherwise
        """
        pass

    @abstractmethod
    def handle_input(self, content: str) -> Tuple[str, str]:
        """
        Handle input content and return (result, log).
        """
        pass
