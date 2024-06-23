from pathlib import Path

from loguru import logger


def init_logger(log_file_name: str, **kwargs) -> None:
    """初始化Logger配置。

    Args:
        log_file_name: 日志文件名。
    """
    log_dir: Path = Path("logs")
    logger.add(log_dir / log_file_name, **kwargs)
