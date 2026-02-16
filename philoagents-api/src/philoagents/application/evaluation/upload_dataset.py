import json
import opik
from pathlib import Path
from philoagents.infrastructure import opik_utils


def upload_dataset(name: str, data_path: Path) -> opik.Dataset:

    with open(data_path, "r") as f:
        data = json.load(f)

    dataset_items = []

    for sample in data['samples']:
        dataset_items.append({"philosopher_id": sample['philosopher_id'],
                              "messages": sample['messages']})
    dataset = opik_utils.create_dataset(name=name,
                                        description="Dataset containing question-answer pairs for multiple philosophers.",
                                        items=dataset_items)

    return dataset