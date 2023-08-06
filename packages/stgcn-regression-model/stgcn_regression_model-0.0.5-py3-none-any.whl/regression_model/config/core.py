from typing import Dict, List, Sequence

from pathlib import Path
from pydantic import BaseModel
from strictyaml import YAML, load

import regression_model

# Directory
PACKAGE_ROOT = Path(regression_model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "data"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "save_model"
TEST_DATA_DIR = PACKAGE_ROOT / 'train_val_test'
PLOT_DIR = PACKAGE_ROOT / 'plots'


class ModelConfig(BaseModel):
    package_name: str
    epochs: int
    plot_stop_num: int
    train_plot: bool
    test_size: float
    n_his: int
    test_model: str
    test_plot: bool

class Config(BaseModel):
    model_config: ModelConfig


def find_config_file() -> Path:
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f'Config not found at {CONFIG_FILE_PATH}')


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def validation_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        model_config=ModelConfig(**parsed_config.data),
    )

    return _config

config = validation_config()
print("PACKAGE_ROOT: ", PACKAGE_ROOT)