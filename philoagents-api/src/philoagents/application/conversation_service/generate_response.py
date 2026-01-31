import uuid
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
from typing import Any, Union
from philoagents.application.conversation_service.workflow.state import PhilosopherState
from philoagents.application.conversation_service.workflow.graph import create_workflow_graph
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from philoagents.config import settings
#from opik.integrations.langchain import OpikTracer

# # Workaround for langchain.debug attribute error
# try:
#     import langchain
#     if not hasattr(langchain, 'debug'):
#         langchain.debug = False
# except ImportError:
#     pass

async def get_response(messages: str | list[str] | list[dict[str, Any]],
                 philosopher_id: str,
                 philosopher_name: str,
                 philosopher_perspective: str,
                 philosopher_style: str,
                 philosopher_context: str,
                 new_thread: bool = False) -> tuple[str, PhilosopherState]:

    graph_builder = create_workflow_graph()

    try:
        # MongoDBSaver uses a synchronous context manager, but works fine in async functions
        # Note: AsyncMongoDBSaver is not available in version 0.1.0
        async with AsyncMongoDBSaver.from_conn_string(
            conn_string=settings.MONGO_URI,
            db_name=settings.MONGO_DB_NAME,
            checkpoint_collection_name=settings.MONGO_STATE_CHECKPOINT_COLLECTION,
            writes_collection_name=settings.MONGO_STATE_WRITES_COLLECTION,
        ) as checkpointer:

            graph = graph_builder.compile(checkpointer=checkpointer)

            #opik_tracer = OpikTracer(graph=graph.get_graph(xray=True))

            thread_id = (
                philosopher_id if not new_thread else f"{philosopher_id}-{uuid.uuid4()}"

            )

            config = {
                "configurable": {
                    "thread_id": thread_id,
                },
                #"callbacks": [opik_tracer],
            }

            output_state = await graph.ainvoke(
                input = {
                        "messages": __format_messages(messages),
                        "philosopher_name": philosopher_name,
                        "philosopher_perspective": philosopher_perspective,
                        "philosopher_style": philosopher_style,
                        "philosopher_context": philosopher_context,
                        },
                config=config
            )

            response = output_state["messages"][-1].content

            return response, PhilosopherState(**output_state)
    except Exception as e:
        raise RuntimeError(f"Error generating response: {e}")



def __format_messages(messages: Union[str, list[str], list[dict[str, Any]]]) -> list[Union[AIMessage, HumanMessage]]:

    if isinstance(messages, str):
        return [HumanMessage(content=messages)]
    
    if isinstance(messages, list):
        if not messages:
            return []
        
        result = []
        if isinstance(messages[0], dict) and "content" in messages[0] and "role" in messages[0]:
            for msg in messages:
                if msg["role"] == "assistant":
                    result.append(AIMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    result.append(HumanMessage(content=msg["content"]))
                else:
                    raise ValueError(f"Invalid message role: {msg['role']}")
            return result

        return [HumanMessage(content=message) for message in messages]


    return []







