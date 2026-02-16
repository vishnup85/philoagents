from philoagents.application.evaluation import upload_dataset, evaluate_agent
from philoagents.config import settings
from pathlib import Path
import click


@click.command()
@click.option("--name", 
                default="philoagents-evaluation-dataset", 
                type=str, 
                help="Name of the dataset")
@click.option("--data-path",
                default=settings.EVALUATION_DATASET_FILE_PATH,
                type=Path, 
                help="Path to the dataset")
@click.option("--workers", default=1, type=int, help="Number of workers")
@click.option("--nb-samples", default=20, type=int, help="Number of samples")
def main(name: str, data_path: Path, workers: int, nb_samples: int):
    dataset = upload_dataset(name=name, data_path=data_path)
    evaluate_agent(dataset=dataset, workers=workers, nb_samples=nb_samples)

if __name__ == "__main__":
    main()