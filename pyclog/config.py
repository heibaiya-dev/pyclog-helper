from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@dataclass
class LogConfig:
    log_file_path: str
    max_file_size: int = 10 * 1024 * 1024
    backup_count: int = 5
    enable_date_rotation: bool = False
    date_format: str = "%Y-%m-%d"
    time_format: str = "%Y-%m-%d %H:%M:%S"
    log_format: str = "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s"
    auto_create_directory: bool = True
    encoding: str = "utf-8"
    min_log_level: LogLevel = LogLevel.DEBUG


@dataclass
class LogMessage:
    level: LogLevel
    message: str
    module_name: str
    timestamp: str
    extra_fields: dict = field(default_factory=dict)


DEFAULT_CONFIG = LogConfig(
    log_file_path="app.log",
    max_file_size=10 * 1024 * 1024,
    backup_count=5,
    enable_date_rotation=False,
    date_format="%Y-%m-%d",
    time_format="%Y-%m-%d %H:%M:%S",
    log_format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
    auto_create_directory=True,
    encoding="utf-8",
    min_log_level=LogLevel.DEBUG
)


def Validate_Config(config: LogConfig) -> bool:
    if not config.log_file_path:
        raise ValueError("log_file_path cannot be empty")
    
    if config.max_file_size <= 0:
        raise ValueError("max_file_size must be greater than 0")
    
    if config.backup_count < 0:
        raise ValueError("backup_count must be non-negative")
    
    if config.backup_count > 100:
        raise ValueError("backup_count should not exceed 100")
    
    return True
