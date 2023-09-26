import os
from unittest import TestCase
from pathlib import Path
from tempfile import TemporaryDirectory

from council_decision.data.handler import YamlHandler

local_path = Path(os.path.dirname(os.path.abspath(__file__)))
tmp_path = Path("/tmp/council_decision/tests/")


class TestYamlHandler(TestCase):
    def test_file_read(self):
        sources = {"a": local_path / "a.yaml", "b": local_path / "b.yaml"}
        with YamlHandler(sources) as data:
            self.assertEqual(data["a"], {"test": True})
            self.assertEqual(data["b"], {"test": True})

    def test_file_write(self):
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            sources = {"a": tmp_path / "a.yaml", "b": tmp_path / "b.yaml"}
            handler = YamlHandler(sources)
            handler.create_sources()
            with handler as data:
                data["a"] = {"test": True}
                data["b"] = {"test": True}
            with handler as data:
                self.assertEqual(data["a"], {"test": True})
                self.assertEqual(data["b"], {"test": True})
