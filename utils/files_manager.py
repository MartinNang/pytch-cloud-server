from pathlib import Path

def get_files_root() -> Path:
    return Path(__file__).parent.parent.joinpath("files").resolve()

def get_test_resources_root() -> Path:
    return Path(__file__).parent.parent.joinpath("test").joinpath("resources").resolve()

def init_files_root() -> Path:
    Path(__file__).parent.parent.joinpath("files").resolve().mkdir(parents=True, exist_ok=True)