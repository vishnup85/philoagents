from langgraph.graph import MessagesState



class PhilosopherState(MessagesState):
    """
    """

    philosopher_context: str
    philosopher_name: str
    philosopher_perspective: str
    philosopher_style: str
    summary: str



def state_to_str(state: PhilosopherState) -> str:

    # LangGraph passes state as a mapping; use .get to avoid KeyError.
    summary = state.get("summary")
    messages = state.get("messages")
    conversation = summary if summary else messages or ""

    return f"""
    PhilosopherState(
        philosopher_context={state.get('philosopher_context')},
        philosopher_name={state.get('philosopher_name')},
        philosopher_perspective={state.get('philosopher_perspective')},
        philosopher_style={state.get('philosopher_style')},
        conversation={conversation}
    )
    """