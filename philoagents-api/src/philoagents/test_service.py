import sys
from pathlib import Path

from philoagents.application.long_term_memory import LongTermMemoryRetriever

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from philoagents.application.conversation_service.generate_response import get_response
from philoagents.application.rag.retrievers import get_retriever
from philoagents.config import settings
import asyncio


def test_rag():
    """Simple RAG test: retrieve documents for a philosopher query."""
    retriever = get_retriever(
        embedding_model_name=settings.RAG_TEXT_EMBEDDING_MODEL,
        k=settings.RAG_TOP_K,
        device=settings.RAG_DEVICE,
    )
    docs = retriever.invoke("Plato's theory of forms")
    print(f"RAG retrieved {len(docs)} documents")
    for i, doc in enumerate(docs[:2], 1):
        print(f"  [{i}] {doc.page_content[:100]}...")


async def main():
    # RAG test
    print("--- RAG Test ---")
    test_rag()
    print()

    messages = "My name is Vishnu, I am a software engineer and I want to learn about philosophy."
    response, state = await get_response(
        messages=messages,
        philosopher_id="plato",
        philosopher_name="Plato",
        philosopher_perspective="Idealism and the Theory of Forms",
        philosopher_style="Socratic",
        philosopher_context="Plato was an ancient Greek philosopher who was a student of Socrates and a teacher of Aristotle. He is considered one of the most important philosophers in history and is known for his theory of forms and his idealism.",
    )
    print('Response:', response)
    print('State:', state)


    ## Testing the memory (same thread_id to load checkpoint from first call)
    messages = "What is my name?"
    response2, state2 = await get_response(
        messages=messages,
        philosopher_id="plato",
        philosopher_name="Plato",
        philosopher_perspective="Idealism and the Theory of Forms",
        philosopher_style="Socratic",
        philosopher_context="Plato was an ancient Greek philosopher who was a student of Socrates and a teacher of Aristotle. He is considered one of the most important philosophers in history and is known for his theory of forms and his idealism.",
    )
    print('Response2:', response2)
    print('State2:', state2)

if __name__ == "__main__":
    asyncio.run(main())