import json
import os
import sys
from pathlib import Path
from typing import Optional

import toml
import yaml

from confz.confz_source import ConfZFileSource, FileFormat
from confz.exceptions import ConfZFileException
from .loader import Loader


class FileLoader(Loader):
    """Config loader for config files."""

    @classmethod
    def _get_filename(cls, confz_source: ConfZFileSource) -> Path:
        if confz_source.file is not None:
            file_path = confz_source.file
        elif confz_source.file_from_env is not None:
            if confz_source.file_from_env not in os.environ:
                raise ConfZFileException(
                    f"Environment variable '{confz_source.file_from_env}' is not set."
                )
            file_path = Path(os.environ[confz_source.file_from_env])
        elif confz_source.file_from_cl is not None:
            if isinstance(confz_source.file_from_cl, int):
                try:
                    file_path = Path(sys.argv[confz_source.file_from_cl])
                except IndexError as e:
                    raise ConfZFileException(
                        f"Command-line argument number {confz_source.file_from_cl} "
                        f"is not set."
                    ) from e
            else:
                try:
                    idx = sys.argv.index(confz_source.file_from_cl)
                except ValueError as e:
                    raise ConfZFileException(
                        f"Command-line argument '{confz_source.file_from_cl}' "
                        f"not found."
                    ) from e
                try:
                    file_path = Path(sys.argv[idx + 1])
                except IndexError as e:
                    raise ConfZFileException(
                        f"Command-line argument '{confz_source.file_from_cl}' is not "
                        f"set."
                    ) from e
        else:
            raise ConfZFileException("No file source set.")

        if confz_source.folder is not None:
            file_path = confz_source.folder / file_path

        return file_path

    @classmethod
    def _get_format(
        cls, file_path: Path, file_format: Optional[FileFormat]
    ) -> FileFormat:
        if file_format is not None:
            return file_format

        suffix_formats = {
            ".yml": FileFormat.YAML,
            ".yaml": FileFormat.YAML,
            ".json": FileFormat.JSON,
            ".toml": FileFormat.TOML,
        }
        suffix = file_path.suffix
        try:
            suffix_format = suffix_formats[suffix]
        except KeyError as e:
            raise ConfZFileException(
                f"File-ending '{suffix}' is not known. Supported are: "
                f"{', '.join(list(suffix_formats.keys()))}."
            ) from e

        return suffix_format

    @classmethod
    def _read_file(
        cls,
        file_path: Path,
        file_format: FileFormat,
        file_encoding: str,
    ) -> dict:
        try:
            with file_path.open(encoding=file_encoding) as f:
                if file_format == FileFormat.YAML:
                    file_content = yaml.safe_load(f)
                elif file_format == FileFormat.JSON:
                    file_content = json.load(f)
                elif file_format == FileFormat.TOML:
                    file_content = toml.load(f)
        except OSError as e:
            raise ConfZFileException(
                f"Could not open config file '{file_path}'."
            ) from e

        return file_content

    @classmethod
    def populate_config(cls, config: dict, confz_source: ConfZFileSource):
        try:
            file_path = cls._get_filename(confz_source)
        except ConfZFileException as e:
            if confz_source.optional:
                return
            raise e
        file_format = cls._get_format(file_path, confz_source.format)
        try:
            file_content = cls._read_file(file_path, file_format, confz_source.encoding)
        except ConfZFileException as e:
            if confz_source.optional:
                return
            raise e
        cls.update_dict_recursively(config, file_content)
