from pathlib import Path

def get_files_root() -> Path:
    return Path(__file__).parent.parent.joinpath("files").resolve()

def init_files_root() -> Path:
    Path(__file__).parent.parent.joinpath("files").resolve().mkdir(parents=True, exist_ok=True)