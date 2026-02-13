from typing import List, Generator, Tuple
from philoagents.domain.philosopher import Philosopher, PhilosopherExtract
from philoagents.domain.philosopher_factory import PhilosopherFactory
from langchain_core.documents import Document
from tqdm import tqdm
from langchain_community.document_loaders import WebBaseLoader, WikipediaLoader


def get_extraction_generator(philosophers: List[PhilosopherExtract]) -> Generator[Tuple[Philosopher, List[Document]], None, None]:
    

    progress_bar = tqdm(
        philosophers,
        desc="Extracting documents",
        unit="philosopher",
        bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}"
    )

    philosopher_factory = PhilosopherFactory()
    for philosopher_extract in progress_bar:
        philosopher = philosopher_factory.get_philosopher(philosopher_extract.id)

        progress_bar.set_postfix_str(f"Philosopher: {philosopher.name}")

        philosopher_documents = extract(philosopher, philosopher_extract.urls)

        yield philosopher, philosopher_documents


def extract(philosopher: Philosopher, extract_urls: List[str]) -> List[Document]:

    docs = []
    docs.extend(extract_wikipedia(philosopher))
    docs.extend(extract_stanford_encyclopedia_of_philosophy(philosopher, extract_urls))

    return docs


def extract_wikipedia(philosopher: Philosopher) -> List[Document]:
    loader = WikipediaLoader(query=philosopher.name,  lang="en",
        load_max_docs=1,
        doc_content_chars_max=1000000
    )
    docs = loader.load()

    for doc in docs:
        doc.metadata["philosopher_id"] = philosopher.id
        doc.metadata["philosopher_name"] = philosopher.name

    return docs

def extract_stanford_encyclopedia_of_philosophy(philosopher: Philosopher, extract_urls: List[str]) -> List[Document]:
    def extract_paragraphs_and_headers(soup) -> str:
        # List of class/id names specific to the Stanford Encyclopedia of Philosophy that we want to exclude.
        excluded_sections = [
            "bibliography",
            "academic-tools",
            "other-internet-resources",
            "related-entries",
            "acknowledgments",
            "article-copyright",
            "article-banner",
            "footer",
        ]

        # Find and remove elements within excluded sections
        for section_name in excluded_sections:
            for section in soup.find_all(id=section_name):
                section.decompose()

            for section in soup.find_all(class_=section_name):
                section.decompose()

            for section in soup.find_all(
                lambda tag: tag.has_attr("id") and section_name in tag["id"].lower()
            ):
                section.decompose()

            for section in soup.find_all(
                lambda tag: tag.has_attr("class")
                and any(section_name in cls.lower() for cls in tag["class"])
            ):
                section.decompose()

        # Extract remaining paragraphs and headers
        content = []
        for element in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
            content.append(element.get_text())

        return "\n\n".join(content)


    if len(extract_urls) == 0:
        return []

    loader = WebBaseLoader(show_progress=False)
    soups = loader.scrape_all(extract_urls)
    docs = []
    for url, soup in zip(extract_urls, soups):
        content = extract_paragraphs_and_headers(soup)
        metadata = {
            "philosopher_id": philosopher.id,
            "philosopher_name": philosopher.name,
            "source": url
        }
        if title := soup.find("title"):
            metadata["title"] = title.get_text().strip(" \n")
        docs.append(Document(page_content=content, metadata=metadata))

    return docs


if __name__ == "__main__":
    aristotle = PhilosopherFactory().get_philosopher("aristotle")
    docs = extract_stanford_encyclopedia_of_philosophy(aristotle, [
            "https://plato.stanford.edu/entries/aristotle/",
            "https://plato.stanford.edu/entries/aristotle/",
        ])
    print(docs)