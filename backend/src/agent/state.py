"""Shared state and typed dictionary definitions for the agent workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict

from langgraph.graph import add_messages
from typing_extensions import Annotated


import operator


class OverallState(TypedDict):
    """Aggregated state shared across the entire agent run."""

    messages: Annotated[list, add_messages]
    search_query: Annotated[list, operator.add]
    web_research_result: Annotated[list, operator.add]
    sources_gathered: Annotated[list, operator.add]
    initial_search_query_count: int
    max_research_loops: int
    research_loop_count: int
    reasoning_model: str


class ReflectionState(TypedDict):
    """State returned from the reflection step."""
    is_sufficient: bool
    knowledge_gap: str
    follow_up_queries: Annotated[list, operator.add]
    research_loop_count: int
    number_of_ran_queries: int


class Query(TypedDict):
    """Structure representing a single search query."""
    query: str
    rationale: str


class QueryGenerationState(TypedDict):
    """State produced when generating search queries."""
    search_query: list[Query]


class WebSearchState(TypedDict):
    """State for a single web search invocation."""
    search_query: str
    id: str


@dataclass(kw_only=True)
class SearchStateOutput:
    """Output returned after finalizing the research workflow."""

    running_summary: str = field(default=None)  # Final report
