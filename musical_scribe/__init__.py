"""
Musical Scribe Architecture

A context-aware musical enhancement system inspired by Sully.ai's medical scribe model.
Transforms YesAnd Music from command-driven to context-driven musical collaboration.
"""

from .project_state_parser import ProjectStateParser
from .musical_context_engine import MusicalContextEngine
from .contextual_prompt_builder import ContextualPromptBuilder
from .musical_scribe_engine import MusicalScribeEngine

__all__ = [
    'ProjectStateParser',
    'MusicalContextEngine', 
    'ContextualPromptBuilder',
    'MusicalScribeEngine'
]
