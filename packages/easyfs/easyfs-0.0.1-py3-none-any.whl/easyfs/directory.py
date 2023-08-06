from typing import Any, Dict, Mapping, Optional, Union
import tempfile
import fsspec
from easyfs.file import File
import os
from flatdict import FlatDict


class Directory(FlatDict):
    def __init__(self, dictionary: Optional[Mapping[str, Union[File, "Directory"]]] = None, metadata: Any = None, allow_override: bool = False):
        super(Directory, self).__init__(dictionary, delimiter="/")
        self.metadata = metadata
        self.allow_override = allow_override

    def create(self, path: str) -> None:
        local_mapper = fsspec.get_mapper(f"file://{path}")
        for k, v in self.as_dict().items():
            assert isinstance(v, File)
            local_mapper[k] = v.content

    def __setitem__(self, key: str, value: Union[File, "Directory"]):
        if key in self and not self.allow_override:
            raise ValueError("no override")
            
        if key == ".":
            raise ValueError(f"not allowed file name: {key}")
        super(Directory, self).__setitem__(key, value)

    def as_dict(self) -> Dict[str, File]:
        return dict(self)

    @classmethod
    def from_local(cls, path: str) -> "Directory":
        local_mapper = fsspec.get_mapper(f"file://{os.path.abspath(path)}")
        return cls(local_mapper)

    @classmethod
    def from_cookiecutter(
        cls,
        template: str,
        config_file: Optional[str] = None,
        default_config: Optional[Dict[str, Any]] = None,
        extra_context: Optional[Dict[str, Any]] = None,
        directory: Optional[str] = None,
        password: Optional[str] = None,
    ) -> "Directory":
        try:
            from cookiecutter.cli import cookiecutter
        except ImportError:
            raise ValueError("cookiecutter is not installed")

        with tempfile.TemporaryDirectory() as temp_dir:
            cookiecutter(
                template=template,
                no_input=True,
                output_dir=temp_dir,
                config_file=config_file,
                default_config=default_config,
                directory=directory,
                extra_context=extra_context,
                password=password,
            )
            return cls.from_local(temp_dir)
