#!/usr/bin/env python3
import sys
import os
sys.path.append('.ai')

from agents.base_agent import PatternFirstAgent
from typing import Dict

class FrontendUIAgent(PatternFirstAgent):
    """Agent for frontend UI components - searches and uses patterns only"""
    
    def __init__(self):
        super().__init__('frontend')
    
    def create_pattern(self, task: str) -> Dict:
        """
        Frontend UI agent should NOT create patterns inline.
        Patterns should be created separately and stored in the library.
        """
        raise NotImplementedError(
            f"Frontend UI agent cannot create patterns inline for: {task}\n"
            "Patterns must be created separately and added to .ai/patterns/frontend/\n"
            "Use: python3 .ai/orchestrator.py create '{task}' to create a pattern manually"
        )

if __name__ == "__main__":
    agent = FrontendUIAgent()
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "create homepage"
    result = agent.execute(task)
    print(result)