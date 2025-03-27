from typing import Dict, List, Type
import importlib
import pkgutil
from pathlib import Path

from ..agents.base import BaseAgent


class AgentRegistry:
    """Registry for managing and discovering agents."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._agents: Dict[str, Type[BaseAgent]] = {}
            self._initialized = True
    
    def register(self, agent_cls: Type[BaseAgent]) -> None:
        """Register a new agent class.
        
        Args:
            agent_cls: The agent class to register
        """
        instance = agent_cls()
        self._agents[instance.name] = agent_cls
    
    def get_agent(self, name: str) -> Type[BaseAgent]:
        """Get an agent class by name.
        
        Args:
            name: Name of the agent to retrieve
            
        Returns:
            The agent class
            
        Raises:
            KeyError: If no agent with the given name exists
        """
        if name not in self._agents:
            raise KeyError(f"No agent registered with name: {name}")
        return self._agents[name]
    
    def list_agents(self) -> List[BaseAgent]:
        """List all registered agents.
        
        Returns:
            List of instantiated agents
        """
        return [agent_cls() for agent_cls in self._agents.values()]
    
    def discover_agents(self) -> None:
        """Discover and register agents from the agents package."""
        agents_path = Path(__file__).parent.parent / "agents"
        plugins_path = Path(__file__).parent.parent / "plugins"
        
        # Discover built-in agents
        for module_info in pkgutil.iter_modules([str(agents_path)]):
            if not module_info.name.startswith("_"):  # Skip __init__.py etc
                module = importlib.import_module(f"..agents.{module_info.name}", package=__package__)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    try:
                        if (isinstance(item, type) and 
                            issubclass(item, BaseAgent) and 
                            item != BaseAgent):
                            self.register(item)
                    except TypeError:
                        continue
        
        # Discover plugin agents if plugins directory exists
        if plugins_path.exists():
            for module_info in pkgutil.iter_modules([str(plugins_path)]):
                if not module_info.name.startswith("_"):
                    module = importlib.import_module(f"..plugins.{module_info.name}", package=__package__)
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        try:
                            if (isinstance(item, type) and 
                                issubclass(item, BaseAgent) and 
                                item != BaseAgent):
                                self.register(item)
                        except TypeError:
                            continue 