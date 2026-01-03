from pydantic import BaseModel, Field
from pathlib import Path
import json

class PhilosopherExtract(BaseModel):
    id: str = Field(..., description="The unique identifier of the philosopher")
    urls: list[str] = Field(..., description="The list of URLs with information about the philosopher")

    @classmethod
    def from_json(cls, metadata_file: Path) -> list["PhilosopherExtract"]:
        with open(metadata_file, 'r') as file:
            philosophers_data = json.load(file)

        return [cls(**philosopher) for philosopher in philosophers_data]





class Philosopher(BaseModel):
    id: str = Field(..., description="The unique identifier of the philosopher")
    name: str = Field(..., description="The name of the philosopher")
    perspective: str = Field(..., description="Description of the philosopher's theoretical views about AI")
    style: str = Field(..., description="Description of the philosopher's talking style")

    def __str__(self) -> str:
        return f"Philosopher(id={self.id}, name={self.name}, perspective={self.perspective}, style={self.style})"


    