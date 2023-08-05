"""Configuration of the SDK module."""
import os
import pathlib
from enum import Enum
from typing import List, Optional, Union

import configargparse  # type: ignore[import]
import pydantic
from pydantic import BaseModel


class SDKMode(str, Enum):
    DEV = "dev"
    PROD = "prod"


class Configuration(BaseModel):
    """Object containing configuration options (see description in fields)."""

    host: pydantic.AnyHttpUrl = pydantic.Field(..., description="Classiq backend URI.")
    should_check_host: bool = pydantic.Field(
        default=True, description="Should check backend URI and version."
    )
    mode: SDKMode = pydantic.Field(
        default=SDKMode.PROD, description="The operational mode of the SDK"
    )


_DEFAULT_CONFIG_FILES = [str(pathlib.Path("classiq", "config.ini"))]
if os.name == "posix":
    # Unix convensions:
    #   System-wide configuration rests in "/etc"
    #       either as "/etc/program_name.conf" or as "/etc/program_name/some_name"
    #   User-wide configuration rests in "~/.config"
    # Order matters - System-wide is most general, than user-wide,
    #   and than folder-specific configration
    _DEFAULT_CONFIG_FILES = [
        "/etc/classiq/config.ini",
        "/etc/classiq.conf",
        "~/.config/classiq/config.ini",
        "~/.config/classiq.conf",
    ] + _DEFAULT_CONFIG_FILES


def init(args: Optional[Union[str, List[str]]] = None) -> Configuration:
    """Initialize the configuration object.

    Args:
        args (): Non-default arguments.

    Returns:
        Initialized configuration object.
    """
    arg_parser = configargparse.ArgParser(default_config_files=_DEFAULT_CONFIG_FILES)

    arg_parser.add_argument(
        "--classiq-config-file",
        is_config_file=True,
        help="Configuration file path",
        env_var="CLASSIQ_CONFIG_FILE",
    )
    arg_parser.add_argument(
        "--classiq-host",
        help="The URL of Classiq's backend host",
        env_var="CLASSIQ_HOST",
        default="https://classiquantum.com",
    )
    arg_parser.add_argument(
        "--classiq-skip-check-host",
        dest="classiq_skip_check_host",
        help="Should skip classiq host and version",
        env_var="CLASSIQ_SKIP_CHECK_HOST",
        action="store_true",
    )
    arg_parser.add_argument(
        "--classiq-mode",
        dest="classiq_mode",
        help="Classiq SDK mode",
        env_var="CLASSIQ_SDK_MODE",
        type=SDKMode,
        default=SDKMode.PROD,
    )

    parsed_args, _ = arg_parser.parse_known_args(args=args)
    return Configuration(
        host=parsed_args.classiq_host,
        should_check_host=not parsed_args.classiq_skip_check_host,
        mode=parsed_args.classiq_mode,
    )
