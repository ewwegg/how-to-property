#!/usr/bin/env python3
import sys
import os
sys.path.append('.ai')

from agents.base_agent import PatternFirstAgent
from typing import Dict

class InfrastructureAgent(PatternFirstAgent):
    """Agent for infrastructure and project setup - searches and uses patterns only"""
    
    def __init__(self):
        super().__init__('infrastructure')
    
    def create_pattern(self, task: str) -> Dict:
        """
        Infrastructure agent should NOT create patterns inline.
        Patterns should be created separately and stored in the library.
        """
        raise NotImplementedError(
            f"Infrastructure agent cannot create patterns inline for: {task}\n"
            "Patterns must be created separately and added to .ai/patterns/infrastructure/\n"
            "Use: python3 .ai/orchestrator.py create '{task}' to create a pattern manually"
        )

if __name__ == "__main__":
    agent = InfrastructureAgent()
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "setup nextjs project"
    result = agent.execute(task)
    print(result)