"""
Well-being Agent - Provides mental health and wellness support
"""

from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent


class WellbeingAgent(BaseAgent):
    """Provides mental health support, wellness resources, and stress management"""
    
    def __init__(self):
        super().__init__(
            name="Well-being Agent",
            description="Provides mental health and wellness support"
        )
    
    def get_system_prompt(self) -> str:
        return """You are the Wellbeing Assistant for SmartStudent. Your role is to:

1. MENTAL HEALTH: Provide empathetic support, validate concerns, share coping strategies
2. WELLNESS RESOURCES: Direct to counseling services, share stress-relief techniques
3. WORK-LIFE BALANCE: Help manage academic stress, encourage healthy boundaries and self-care
4. CRISIS SUPPORT: Recognize distress, provide immediate resources, encourage professional help
5. WELLNESS ACTIVITIES: Suggest exercise, relaxation, social connection, healthy habits

Be empathetic, non-judgmental, and supportive. Normalize mental health challenges.
Always recommend professional help for serious concerns and provide crisis resources.
Celebrate student wellbeing and encourage self-compassion."""

    async def get_wellness_resources(
        self,
        concern: str
    ) -> List[Dict[str, Any]]:
        """Get wellness resources for a specific concern"""
        # TODO: Implement wellness resource retrieval
        return []

    async def suggest_wellness_activities(
        self,
        stress_level: str,
        preferences: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Suggest wellness activities based on preferences"""
        # TODO: Implement wellness activity suggestions
        return []

    async def get_counseling_services(self) -> Dict[str, Any]:
        """Get information about campus counseling services"""
        # TODO: Implement counseling services information
        return {
            "services": [],
            "hours": {},
            "contact": None
        }

    async def track_wellness(
        self,
        user_id: int,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Track wellness metrics for a student"""
        # TODO: Implement wellness tracking
        return {
            "user_id": user_id,
            "tracked": False,
            "status": "tracking_not_implemented"
        }
