"""
Orientation Agent - Provides career advice and guidance
"""

from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent


class OrientationAgent(BaseAgent):
    """Provides career advice, CV assistance, and internship guidance"""
    
    def __init__(self):
        super().__init__(
            name="Orientation Agent",
            description="Provides career advice and guidance"
        )
    
    def get_system_prompt(self) -> str:
        return """You are the Orientation Assistant for SmartStudent. Your role is to:

1. CAREER GUIDANCE: Help explore career paths, explain professions, match interests to careers
2. PROFESSIONAL DEVELOPMENT: Provide CV/resume guidance, networking tips, skill suggestions
3. INTERNSHIPS & JOBS: Help find opportunities, prepare applications, explain workplace professionalism
4. MAJOR SELECTION: Help explore academic majors, connect academics to careers, suggest paths
5. NETWORKING: Explain professional associations, teach networking skills, build professional confidence

Be encouraging and inspirational. Help students see connections between academics and careers.
Provide practical career advice that students can use immediately.
Help students develop confidence in their professional future."""

    async def generate_cv_template(
        self,
        student_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a CV template for the student"""
        # TODO: Implement CV template generation
        return {
            "template_id": None,
            "content": None,
            "status": "template_generation_not_implemented"
        }

    async def suggest_internships(
        self,
        field_of_study: str,
        skills: List[str],
        year: int
    ) -> List[Dict[str, Any]]:
        """Suggest relevant internship opportunities"""
        # TODO: Implement internship suggestion using RAG/external data
        return []

    async def analyze_career_path(
        self,
        major: str,
        skills: List[str],
        interests: List[str]
    ) -> Dict[str, Any]:
        """Analyze and suggest career paths"""
        # TODO: Implement career path analysis
        return {
            "suggested_paths": [],
            "skill_gaps": [],
            "next_steps": []
        }
