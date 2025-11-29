"""Shared memory bank for agent communication."""

from typing import Dict, Any, List


class MemoryBank:
    """Shared memory storage for agents to exchange information."""
    
    def __init__(self, style_guide: str = ""):
        self.style_guide = style_guide
        self.research_data: Dict[str, Any] = {}
        self.drafts: List[str] = []
        self.seo_data: Dict[str, Any] = {}
        self.editor_feedback: List[Dict[str, Any]] = []
        
    def store_research(self, data: Dict[str, Any]) -> None:
        """Store research findings."""
        self.research_data = data
        
    def get_research(self) -> Dict[str, Any]:
        """Retrieve research data."""
        return self.research_data
    
    def add_draft(self, draft: str) -> None:
        """Add a new draft version."""
        self.drafts.append(draft)
        
    def get_latest_draft(self) -> str:
        """Get the most recent draft."""
        return self.drafts[-1] if self.drafts else ""
    
    def get_all_drafts(self) -> List[str]:
        """Get all draft versions."""
        return self.drafts
    
    def store_seo_data(self, data: Dict[str, Any]) -> None:
        """Store SEO optimization data."""
        self.seo_data = data
        
    def get_seo_data(self) -> Dict[str, Any]:
        """Retrieve SEO data."""
        return self.seo_data
    
    def add_editor_feedback(self, feedback: Dict[str, Any]) -> None:
        """Add editor feedback."""
        self.editor_feedback.append(feedback)
        
    def get_latest_feedback(self) -> Dict[str, Any]:
        """Get the most recent editor feedback."""
        return self.editor_feedback[-1] if self.editor_feedback else {}
    
    def get_feedback_count(self) -> int:
        """Get number of editor feedback iterations."""
        return len(self.editor_feedback)
    
    def clear(self) -> None:
        """Clear all memory except style guide."""
        self.research_data = {}
        self.drafts = []
        self.seo_data = {}
        self.editor_feedback = []
