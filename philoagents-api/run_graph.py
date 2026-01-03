import asyncio
import uuid
from langchain_core.messages import HumanMessage
from src.philoagents.application.conversation_service.workflow.graph import graph
from src.philoagents.domain.philosopher import Philosopher


plato = Philosopher(
    id="plato",
    name="Plato",
    perspective="Plato is a philosopher who is known for his theory of forms. He is also known for his theory of the soul.",
    style="Plato is a philosopher who is known for his theory of forms. He is also known for his theory of the soul.",  
)


inputs = {
    "messages": [HumanMessage(content="What is the meaning of life?")],
    "philosopher_name": plato.name,
    "philosopher_perspective": plato.perspective,
    "philosopher_style": plato.style,
    "philosopher_context": "",
    "summary": ""
}


async def main():
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = await graph.ainvoke(inputs, config=config)
    print(result['messages'][-1].content)


if __name__ == "__main__":
    asyncio.run(main())