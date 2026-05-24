"""
SmartStudent Agents Package
Contains the orchestrator and specialist agents
"""

from .orchestrator import orchestrator, Orchestrator
from .base_agent import BaseAgent
from .admin_agent import AdminAgent
from .planning_agent import PlanningAgent
from .exams_agent import ExamsAgent
from .orientation_agent import OrientationAgent
from .campus_agent import CampusAgent
from .wellbeing_agent import WellbeingAgent

__all__ = [
    "orchestrator",
    "Orchestrator",
    "BaseAgent",
    "AdminAgent",
    "PlanningAgent",
    "ExamsAgent",
    "OrientationAgent",
    "CampusAgent",
    "WellbeingAgent",
]
