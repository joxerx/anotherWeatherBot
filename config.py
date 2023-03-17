import os
from dataclasses import dataclass

import yaml
from marshmallow_dataclass import class_schema


@dataclass
class Config:
    REDIS_HOST: str
    REDIS_PORT: int

    YANDEX_API_KEY: str

    BOT_TOKEN: str


config_path = "/config.yaml"


with open(os.path.dirname(__file__) + config_path) as f:
    config_data = yaml.safe_load(f)

config: Config = class_schema(Config)().load(config_data)
