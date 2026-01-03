from typing_extensions import Literal
from langgraph.graph import END
from philoagents.application.conversation_service.workflow.state import PhilosopherState
from philoagents.config import settings

def should_summarize_conversation(state: PhilosopherState) -> Literal["summarize_conversation_node", 
                                                                        "__end__"]:
    """
    Conditional edge function that determines whether to summarize the conversation.
    
    Returns:
        "summarize_conversation_node" if message count exceeds threshold
        "__end__" (END constant) to terminate the graph otherwise
    """
    messages = state['messages']

    if len(messages) > settings.TOTAL_MESSAGES_AFTER_SUMMARY:
        return "summarize_conversation_node"
    else:
        return END  # END is a string constant equal to "__end__"


                                                                    