from pathlib import Path

import click

from philoagents.application import LongTermMemoryCreator
from philoagents.config import settings
from philoagents.domain.philosopher import PhilosopherExtract


@click.command()
@click.option(
    "--metadata-file",
    type=click.Path(exists=True, path_type=Path),
    default=settings.EXTRACTION_METADATA_FILE_PATH,
    help="The file containing the metadata of the philosophers.",
)
def main(metadata_file: Path) -> None:
    philosophers = PhilosopherExtract.from_json(metadata_file)
    long_term_memory_creator = LongTermMemoryCreator.build_from_settings()
    long_term_memory_creator(philosophers)


if __name__ == "__main__":
    main()

