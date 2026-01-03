from functools import lru_cache
from langgraph.graph import START, END, StateGraph

from philoagents.application.conversation_service.workflow.nodes import (
    conversation_node,
    summarize_conversation_node,
    summarize_context_node,
    connector_node,
)

from philoagents.application.conversation_service.workflow.edges import should_summarize_conversation
from philoagents.application.conversation_service.workflow.state import PhilosopherState


@lru_cache(maxsize=1)
def create_workflow_graph():
    """
    Creates and returns the workflow graph.
    
    @lru_cache(maxsize=1) ensures the graph is only created once and cached.
    Since the function takes no parameters, it will always return the same
    cached graph instance on subsequent calls, avoiding expensive re-creation.
    """
    graph_builder = StateGraph(PhilosopherState)

    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    graph_builder.add_node("summarize_context_node", summarize_context_node)
    graph_builder.add_node("connector_node", connector_node)

    graph_builder.add_edge(START, "conversation_node")
    graph_builder.add_edge("conversation_node", "connector_node")
    #graph_builder.add_edge("summarize_context_node", "conversation_node")
    graph_builder.add_conditional_edges(
        "connector_node", should_summarize_conversation)
    

    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder


graph = create_workflow_graph().compile()




