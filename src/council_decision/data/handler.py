from typing import Union, Dict, Any
from pathlib import Path
from abc import ABC, abstractmethod

from council_decision.yaml import load, dump


class Handler(ABC):
    def __init__(self, sources: Dict[str, Any]):
        self.sources: Dict[str, Any] = sources
        self.data: Any = None

    def __enter__(self) -> Any:
        self.data = self.fetch_data()
        return self.data

    def __exit__(self, type, value, traceback):
        self.save_data(self.data)
        self.data = None

    @abstractmethod
    def fetch_data(self) -> Any:
        pass

    @abstractmethod
    def save_data(self, data: Any) -> None:
        pass

    @abstractmethod
    def create_sources(self) -> None:
        pass


class YamlHandler(Handler):
    def __init__(self, sources: Dict[str, Path]):
        self.sources: Dict[str, Path] = sources
        self.data: Any = None

    def fetch_data(self) -> Any:
        data = {}
        for name, file in self.sources.items():
            with open(file) as fh:
                data[name] = load(fh)
        return data

    def save_data(self, data: Any) -> None:
        for name, file in self.sources.items():
            with open(file, "w") as fh:
                dump(self.data[name], fh)

    def create_sources(self) -> None:
        for _, file in self.sources.items():
            if not file.exists():
                file.touch()
