from pydantic import BaseModel


class ModelFile(BaseModel):
    name: str
    gdriver_id: str


class BaseEngine(BaseModel):
    model_instance: str


class Engine(BaseEngine):
    checkpoint_version: str
    files: list[ModelFile]


class EngineList(BaseModel):
    engine_list: list[Engine]
