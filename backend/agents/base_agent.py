"""
Base Agent class - Template for all specialist agents
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from langchain_core.messages import HumanMessage, AIMessage
from backend.config import get_settings

settings = get_settings()


class BaseAgent(ABC):
    """Base class for all specialist agents"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @property
    def llm(self):
        """Always fetch LLM from orchestrator (handles key rotation without restart)."""
        from backend.agents.orchestrator import get_llm
        return get_llm()

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass

    async def process(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        messages = [HumanMessage(content=self.get_system_prompt())]

        if conversation_history:
            for msg in conversation_history:
                if msg.get("role") == "user":
                    messages.append(HumanMessage(content=msg.get("content", "")))
                else:
                    messages.append(AIMessage(content=msg.get("content", "")))

        messages.append(HumanMessage(content=user_message))

        try:
            response = self.llm.invoke(messages)
            return {"response": response.content, "agent": self.name, "success": True}
        except Exception as e:
            return {
                "response": f"Erreur lors du traitement: {str(e)}",
                "agent": self.name,
                "success": False,
                "error": str(e),
            }
